"""PluginLoader – discovers, registers, and applies audio plugins."""
import importlib.util
import json
from pathlib import Path


BUILT_IN_PLUGINS = [
    {
        "name":        "reverb",
        "label":       "Reverb",
        "description": "Adds room / hall reverb to the signal.",
        "params":      {"room_size": 0.5, "damping": 0.4, "wet": 0.3},
        "icon":        "🎧",
        "enabled":     False,
    },
    {
        "name":        "spectrum_visualizer",
        "label":       "Spectrum Visualiser",
        "description": "Real-time frequency spectrum display.",
        "params":      {"bands": 64, "decay": 0.8},
        "icon":        "🌈",
        "enabled":     True,
    },
    {
        "name":        "equalizer",
        "label":       "10-Band EQ",
        "description": "Parametric 10-band equaliser.",
        "params":      {
            "32hz": 0, "64hz": 0, "125hz": 0, "250hz": 0, "500hz": 0,
            "1khz": 0, "2khz": 0, "4khz": 0, "8khz": 0, "16khz": 0
        },
        "icon":        "🎚️",
        "enabled":     True,
    },
    {
        "name":        "compressor",
        "label":       "Compressor",
        "description": "Dynamic range compressor.",
        "params":      {"threshold": -24, "ratio": 4, "attack": 0.003, "release": 0.25},
        "icon":        "⚡",
        "enabled":     False,
    },
    {
        "name":        "pitch_shift",
        "label":       "Pitch Shift",
        "description": "Shift pitch without changing tempo.",
        "params":      {"semitones": 0},
        "icon":        "🎵",
        "enabled":     False,
    },
    {
        "name":        "stereo_enhancer",
        "label":       "Stereo Enhancer",
        "description": "Widens the stereo field.",
        "params":      {"width": 1.2},
        "icon":        "↔️",
        "enabled":     False,
    },
]


class PluginLoader:
    def __init__(self, plugin_dir: Path):
        self.plugin_dir = Path(plugin_dir)
        self._registry: dict = {p["name"]: p.copy() for p in BUILT_IN_PLUGINS}
        self._discover_file_plugins()

    # ── discovery ─────────────────────────────────────────────────────────────
    def _discover_file_plugins(self):
        if not self.plugin_dir.exists():
            return
        for py in self.plugin_dir.glob("*.py"):
            name = py.stem
            if name not in self._registry:
                self._registry[name] = {
                    "name":        name,
                    "label":       name.replace("_", " ").title(),
                    "description": f"External plugin: {name}",
                    "params":      {},
                    "icon":        "🔌",
                    "enabled":     False,
                }

    # ── public ────────────────────────────────────────────────────────────────
    def list_plugins(self) -> list:
        return list(self._registry.values())

    def toggle(self, name: str) -> dict:
        if name not in self._registry:
            return {"error": "Plugin not found"}
        p = self._registry[name]
        p["enabled"] = not p["enabled"]
        state = "enabled" if p["enabled"] else "disabled"
        return {"name": name, "enabled": p["enabled"], "message": f"Plugin {state}"}

    def apply(self, name: str, params: dict) -> dict:
        if name not in self._registry:
            return {"error": "Plugin not found"}
        p = self._registry[name]
        p["params"].update(params)
        return {
            "name":    name,
            "applied": True,
            "params":  p["params"],
            "message": f"{p['icon']} {p['label']} applied",
        }
