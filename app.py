"""
Project Sound – Full Audio Platform
Created by Navajeevan Panthi
Flask Web Application Entry Point
"""

import os
import sys
import json
import time
import hashlib
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory

# ── add sub-modules to path ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from Player.player_core     import PlayerCore
from AI.auto_tagging_ai     import AutoTagger
from AI.noise_filter        import NoiseFilter
from PluginLoader.plugin_loader import PluginLoader
from ThemeEngine.theme_engine   import ThemeEngine

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "projectsound_secret_key"

# ── singletons ───────────────────────────────────────────────────────────────
player   = PlayerCore()
tagger   = AutoTagger()
noise    = NoiseFilter()
plugins  = PluginLoader(BASE_DIR / "Plugins")
themes   = ThemeEngine(BASE_DIR / "ThemeBuilder" / "themes")

UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".dsd"}


# ════════════════════════════════════════════════════════════════════════════
# HTML SHELL (served once; JS drives everything after)
# ════════════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html")


# ════════════════════════════════════════════════════════════════════════════
# LIBRARY  –  upload / list / delete
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/library", methods=["GET"])
def library_list():
    files = []
    for f in sorted(UPLOAD_DIR.iterdir()):
        if f.suffix.lower() in ALLOWED:
            meta = tagger.get_meta(f)
            files.append({
                "id":       hashlib.md5(f.name.encode()).hexdigest()[:8],
                "filename": f.name,
                "url":      f"/static/uploads/{f.name}",
                "size":     f.stat().st_size,
                "format":   f.suffix.upper().lstrip("."),
                "title":    meta.get("title", f.stem),
                "artist":   meta.get("artist", "Unknown Artist"),
                "album":    meta.get("album",  "Unknown Album"),
                "duration": meta.get("duration", 0),
                "bitrate":  meta.get("bitrate", 0),
                "samplerate": meta.get("samplerate", 44100),
                "tags":     meta.get("tags", []),
            })
    return jsonify({"tracks": files, "count": len(files)})


@app.route("/api/library/upload", methods=["POST"])
def library_upload():
    uploaded = []
    for f in request.files.getlist("files"):
        ext = Path(f.filename).suffix.lower()
        if ext not in ALLOWED:
            continue
        dest = UPLOAD_DIR / f.filename
        f.save(dest)
        meta  = tagger.get_meta(dest)
        tags  = tagger.auto_tag(dest)
        uploaded.append({
            "filename": f.filename,
            "title":    meta.get("title", Path(f.filename).stem),
            "artist":   meta.get("artist", "Unknown Artist"),
            "tags":     tags,
            "format":   ext.upper().lstrip(".")
        })
    return jsonify({"uploaded": uploaded, "count": len(uploaded)})


@app.route("/api/library/delete/<filename>", methods=["DELETE"])
def library_delete(filename):
    target = UPLOAD_DIR / filename
    if target.exists() and target.suffix.lower() in ALLOWED:
        target.unlink()
        return jsonify({"deleted": filename})
    return jsonify({"error": "File not found"}), 404


# ════════════════════════════════════════════════════════════════════════════
# METADATA / TAGGING
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/meta/<filename>", methods=["GET"])
def meta_get(filename):
    f = UPLOAD_DIR / filename
    if not f.exists():
        return jsonify({"error": "Not found"}), 404
    return jsonify(tagger.get_meta(f))


@app.route("/api/meta/<filename>", methods=["POST"])
def meta_save(filename):
    f    = UPLOAD_DIR / filename
    data = request.get_json()
    result = tagger.save_meta(f, data)
    return jsonify(result)


@app.route("/api/tag/auto/<filename>", methods=["POST"])
def tag_auto(filename):
    f    = UPLOAD_DIR / filename
    tags = tagger.auto_tag(f)
    return jsonify({"filename": filename, "tags": tags, "message": "AI tagging complete"})


# ════════════════════════════════════════════════════════════════════════════
# AUDIO PROCESSING
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/noise/clean/<filename>", methods=["POST"])
def noise_clean(filename):
    f      = UPLOAD_DIR / filename
    result = noise.clean(f)
    return jsonify(result)


@app.route("/api/waveform/<filename>", methods=["GET"])
def waveform(filename):
    f = UPLOAD_DIR / filename
    data = player.get_waveform(f)
    return jsonify(data)


# ════════════════════════════════════════════════════════════════════════════
# PLUGINS
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/plugins", methods=["GET"])
def plugins_list():
    return jsonify({"plugins": plugins.list_plugins()})


@app.route("/api/plugins/<name>/toggle", methods=["POST"])
def plugin_toggle(name):
    result = plugins.toggle(name)
    return jsonify(result)


@app.route("/api/plugins/<name>/apply", methods=["POST"])
def plugin_apply(name):
    data   = request.get_json() or {}
    result = plugins.apply(name, data)
    return jsonify(result)


# ════════════════════════════════════════════════════════════════════════════
# THEMES
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/themes", methods=["GET"])
def themes_list():
    return jsonify({"themes": themes.list_themes()})


@app.route("/api/themes/<name>", methods=["GET"])
def theme_get(name):
    t = themes.get_theme(name)
    return jsonify(t)


@app.route("/api/themes", methods=["POST"])
def theme_save():
    data = request.get_json()
    result = themes.save_theme(data)
    return jsonify(result)


# ════════════════════════════════════════════════════════════════════════════
# BUILD CONSOLE
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/build/<target>", methods=["POST"])
def build(target):
    from Scripts.build_exe import simulate_exe_build
    from Scripts.build_apk import simulate_apk_build
    logs = []
    if target in ("exe", "all"):
        logs += simulate_exe_build()
    if target in ("apk", "all"):
        logs += simulate_apk_build()
    return jsonify({"target": target, "logs": logs, "status": "success"})


# ════════════════════════════════════════════════════════════════════════════
# PLAYER STATUS (polled by JS)
# ════════════════════════════════════════════════════════════════════════════
@app.route("/api/player/status", methods=["GET"])
def player_status():
    return jsonify(player.status())


if __name__ == "__main__":
    print("\n" + "═"*52)
    print("  🎵  PROJECT SOUND  –  Admin Console")
    print("  Open  http://127.0.0.1:5000  in your browser")
    print("═"*52 + "\n")
    app.run(debug=True, port=5000)
