"""ThemeEngine – manages colour themes for Project Sound."""
import json
from pathlib import Path

DEFAULT_THEMES = {
    "default": {
        "name":       "Default Dark",
        "background": "#121212",
        "surface":    "#1E1E1E",
        "panel":      "#282828",
        "text":       "#FFFFFF",
        "subtext":    "#B3B3B3",
        "accent":     "#1DB954",
        "accent2":    "#1ED760",
        "danger":     "#E74C3C",
        "warning":    "#F39C12",
    },
    "midnight": {
        "name":       "Midnight Blue",
        "background": "#0A0E1A",
        "surface":    "#111827",
        "panel":      "#1F2937",
        "text":       "#F9FAFB",
        "subtext":    "#9CA3AF",
        "accent":     "#3B82F6",
        "accent2":    "#60A5FA",
        "danger":     "#EF4444",
        "warning":    "#F59E0B",
    },
    "sunset": {
        "name":       "Sunset",
        "background": "#1A0A0A",
        "surface":    "#271111",
        "panel":      "#3B1515",
        "text":       "#FFF5F5",
        "subtext":    "#FCA5A5",
        "accent":     "#F97316",
        "accent2":    "#FB923C",
        "danger":     "#E11D48",
        "warning":    "#FBBF24",
    },
    "violet": {
        "name":       "Violet Night",
        "background": "#0F0A1E",
        "surface":    "#1A1030",
        "panel":      "#261845",
        "text":       "#EDE9FE",
        "subtext":    "#C4B5FD",
        "accent":     "#8B5CF6",
        "accent2":    "#A78BFA",
        "danger":     "#F43F5E",
        "warning":    "#FCD34D",
    },
}


class ThemeEngine:
    def __init__(self, theme_dir: Path):
        self.theme_dir = Path(theme_dir)
        self.theme_dir.mkdir(parents=True, exist_ok=True)
        self._themes = {k: v.copy() for k, v in DEFAULT_THEMES.items()}
        self._load_user_themes()

    def _load_user_themes(self):
        for f in self.theme_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                self._themes[f.stem] = data
            except Exception:
                pass

    def list_themes(self) -> list:
        return [{"key": k, **v} for k, v in self._themes.items()]

    def get_theme(self, name: str) -> dict:
        return self._themes.get(name, self._themes["default"])

    def save_theme(self, data: dict) -> dict:
        key = data.get("key") or data.get("name", "custom").lower().replace(" ", "_")
        self._themes[key] = data
        out = self.theme_dir / f"{key}.json"
        out.write_text(json.dumps(data, indent=2))
        return {"saved": True, "key": key}
