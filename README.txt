Welcome to Project Sound – Full DevKit v2.0
Created by Navajeevan Panthi
============================================

QUICK START
-----------
1. Install Python 3.10+
2. Open terminal in this folder
3. Run:  pip install -r requirements.txt
4. Run:  python app.py
5. Open: http://127.0.0.1:5000

Or use the launchers:
  Windows:       run.bat
  macOS / Linux: bash run.sh
  Admin entry:   python AdminConsole/admin_console_gui.py

FEATURES
--------
✅  Library       – Upload FLAC, DSD, MP3, MQA, WAV, AAC, OGG, Opus
✅  Player        – HTML5 audio with waveform + real-time spectrum
✅  Metadata      – AI auto-tagging + manual editor (mutagen)
✅  AI Noise      – Noise reduction with profile detection
✅  EQ & Effects  – 10-band EQ, compressor, reverb (8 presets)
✅  Plugins       – 6 built-in plugins with live parameter control
✅  Themes        – 4 built-in themes + custom theme builder
✅  Build Console – Simulated EXE / APK / macOS / iOS builds

PROJECT STRUCTURE
-----------------
app.py                  – Flask server (main entry)
Player/player_core.py   – Waveform extraction
AI/auto_tagging_ai.py   – AI metadata tagger
AI/noise_filter.py      – Noise reduction module
PluginLoader/           – Plugin discovery & registry
Plugins/                – reverb, spectrum, EQ, compressor…
ThemeEngine/            – Theme management
ThemeBuilder/themes/    – JSON theme files
Scripts/                – Build simulators (EXE, APK)
templates/index.html    – Full single-page frontend
static/uploads/         – Uploaded audio files

SUPPORTED FORMATS
-----------------
FLAC · DSD · MP3 · MQA · WAV · AAC · M4A · OGG · Opus
