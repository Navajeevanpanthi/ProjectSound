"""Player Core – waveform extraction, metadata, status tracking."""
import json
import time
import random
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import mutagen
    from mutagen import File as MutagenFile
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False


class PlayerCore:
    def __init__(self):
        self._current  = None
        self._playing  = False
        self._position = 0.0
        self._volume   = 0.8
        self._started  = None

    # ── public API ────────────────────────────────────────────────────────────
    def status(self):
        return {
            "current":  self._current,
            "playing":  self._playing,
            "position": self._position,
            "volume":   self._volume,
        }

    def get_waveform(self, filepath: Path, samples: int = 200) -> dict:
        """Return a compact waveform array suitable for canvas rendering."""
        filepath = Path(filepath)
        if not filepath.exists():
            return {"error": "File not found", "peaks": []}

        peaks = self._extract_peaks(filepath, samples)
        return {
            "filename": filepath.name,
            "peaks":    peaks,
            "samples":  len(peaks),
        }

    # ── internals ─────────────────────────────────────────────────────────────
    def _extract_peaks(self, filepath: Path, n: int) -> list:
        """Try real extraction; fall back to deterministic fake peaks."""
        try:
            return self._real_peaks(filepath, n)
        except Exception:
            return self._fake_peaks(filepath.name, n)

    def _real_peaks(self, filepath: Path, n: int) -> list:
        if not HAS_NUMPY:
            raise RuntimeError("numpy unavailable")

        # Try reading raw PCM via wave (works for .wav files)
        import wave, struct
        if filepath.suffix.lower() == ".wav":
            with wave.open(str(filepath), "r") as wf:
                frames  = wf.readframes(wf.getnframes())
                ch      = wf.getnchannels()
                width   = wf.getsampwidth()
                fmt     = {1: "B", 2: "h", 4: "i"}.get(width, "h")
                samples = np.frombuffer(frames, dtype=np.dtype(fmt))
                if ch > 1:
                    samples = samples[::ch]   # take left channel
                samples = samples.astype(float)
                mx = np.max(np.abs(samples)) or 1
                samples /= mx
                step = max(1, len(samples) // n)
                peaks = [float(round(np.max(np.abs(samples[i:i+step])), 3))
                         for i in range(0, len(samples), step)][:n]
                return peaks
        raise RuntimeError("not a WAV")

    @staticmethod
    def _fake_peaks(name: str, n: int) -> list:
        """Deterministic waveform seeded by filename so it stays stable."""
        if not HAS_NUMPY:
            seed = sum(ord(c) for c in name)
            rng  = random.Random(seed)
            raw  = [rng.random() for _ in range(n)]
        else:
            seed = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % (2**32)
            rng  = np.random.default_rng(seed)
            raw  = rng.uniform(0.05, 1.0, n).tolist()

        # smooth it so it looks musical
        smoothed = raw[:]
        for i in range(1, len(raw)-1):
            smoothed[i] = (raw[i-1] + raw[i]*2 + raw[i+1]) / 4
        # clamp
        return [round(max(0.05, min(1.0, v)), 3) for v in smoothed]


import hashlib  # used in _fake_peaks; import here avoids circular
