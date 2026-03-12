"""Auto-tagging AI – reads embedded metadata + applies heuristic/AI tags."""
import re
import hashlib
from pathlib import Path

try:
    from mutagen import File as MutagenFile
    from mutagen.mp3  import MP3
    from mutagen.flac import FLAC
    from mutagen.id3  import ID3, TIT2, TPE1, TALB, TCON, TDRC, ID3NoHeaderError
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

# ── heuristic genre/mood vocabulary ──────────────────────────────────────────
_GENRE_HINTS = {
    "rock":       ["guitar", "rock", "band", "live"],
    "jazz":       ["jazz", "trumpet", "sax", "blues", "swing"],
    "classical":  ["symphony", "opus", "concerto", "sonata", "suite", "quartet"],
    "electronic": ["edm", "synth", "beat", "techno", "house", "trance"],
    "hip-hop":    ["rap", "hiphop", "hip_hop", "trap", "freestyle"],
    "pop":        ["pop", "single", "chart", "radio"],
    "ambient":    ["ambient", "chill", "lofi", "lo-fi", "relax"],
    "metal":      ["metal", "heavy", "thrash", "doom"],
    "folk":       ["folk", "acoustic", "indie", "country"],
}

_MOOD_MAP = {
    "major": "uplifting",
    "minor": "melancholic",
    "fast":  "energetic",
    "slow":  "calm",
}

_FORMAT_TAGS = {
    ".flac": ["lossless", "hi-res"],
    ".dsd":  ["lossless", "hi-res", "DSD"],
    ".wav":  ["lossless", "PCM"],
    ".mp3":  ["compressed", "lossy"],
    ".aac":  ["compressed", "lossy"],
    ".m4a":  ["compressed", "lossy"],
    ".ogg":  ["compressed", "open-source"],
    ".opus": ["compressed", "low-bitrate"],
}


class AutoTagger:
    # ── metadata read ─────────────────────────────────────────────────────────
    def get_meta(self, filepath) -> dict:
        filepath = Path(filepath)
        meta = {
            "title":      filepath.stem,
            "artist":     "Unknown Artist",
            "album":      "Unknown Album",
            "genre":      "",
            "year":       "",
            "duration":   0,
            "bitrate":    0,
            "samplerate": 44100,
            "channels":   2,
            "tags":       [],
            "format":     filepath.suffix.upper().lstrip("."),
        }
        if not HAS_MUTAGEN or not filepath.exists():
            return meta

        try:
            af = MutagenFile(str(filepath), easy=True)
            if af is None:
                return meta

            def _first(key):
                v = af.tags.get(key) if af.tags else None
                return str(v[0]) if v else ""

            meta["title"]  = _first("title")  or filepath.stem
            meta["artist"] = _first("artist") or "Unknown Artist"
            meta["album"]  = _first("album")  or "Unknown Album"
            meta["genre"]  = _first("genre")
            meta["year"]   = _first("date")

            if hasattr(af, "info"):
                info = af.info
                meta["duration"]   = round(getattr(info, "length",     0), 2)
                meta["bitrate"]    = getattr(info, "bitrate",    0)
                meta["samplerate"] = getattr(info, "sample_rate", 44100)
                meta["channels"]   = getattr(info, "channels",    2)
        except Exception:
            pass

        return meta

    # ── metadata write ────────────────────────────────────────────────────────
    def save_meta(self, filepath, data: dict) -> dict:
        filepath = Path(filepath)
        if not HAS_MUTAGEN or not filepath.exists():
            return {"saved": False, "reason": "mutagen unavailable or file missing"}

        try:
            af = MutagenFile(str(filepath), easy=True)
            if af is None:
                return {"saved": False, "reason": "Unsupported format"}
            if af.tags is None:
                af.add_tags()
            for key in ("title", "artist", "album", "genre", "date"):
                if key in data and data[key]:
                    af.tags[key] = data[key]
            af.save()
            return {"saved": True, "filename": filepath.name}
        except Exception as e:
            return {"saved": False, "reason": str(e)}

    # ── AI / heuristic tagging ────────────────────────────────────────────────
    def auto_tag(self, filepath) -> list:
        filepath = Path(filepath)
        tags: set = set()

        # format tags
        tags.update(_FORMAT_TAGS.get(filepath.suffix.lower(), []))

        # name-based heuristics
        slug = re.sub(r"[^a-z0-9 ]", " ", filepath.stem.lower())
        for genre, hints in _GENRE_HINTS.items():
            if any(h in slug for h in hints):
                tags.add(genre)

        # metadata-based
        meta = self.get_meta(filepath)
        if meta.get("genre"):
            tags.add(meta["genre"].lower().split("/")[0].strip())
        if meta.get("bitrate", 0) > 300:
            tags.add("high-quality")
        if meta.get("samplerate", 0) >= 96000:
            tags.add("hi-res")
        if meta.get("duration", 0) > 600:
            tags.add("long-form")

        return sorted(tags)
