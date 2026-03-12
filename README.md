# 🎵 ProjectSound

**An Audiophile's All-in-One Suite** — a Python/Flask-based audio platform with AI-powered features, real-time effects, a plugin system, and a fully customizable theme engine.

---

## 🚀 Quick Start

### Requirements
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Navajeevanpanthi/ProjectSound.git
cd ProjectSound

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open your browser at: **http://127.0.0.1:5000**

### Platform Launchers
| Platform | Command |
|----------|---------|
| Windows | `run.bat` |
| macOS / Linux | `bash run.sh` |
| Admin Console | `python AdminConsole/admin_console_gui.py` |

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📁 **Library** | Upload and manage your audio collection |
| ▶️ **Player** | HTML5 audio with waveform + real-time spectrum visualizer |
| 🤖 **AI Metadata** | Auto-tagging with manual editor (powered by mutagen) |
| 🔇 **AI Noise Reduction** | Smart noise reduction with automatic profile detection |
| 🎚️ **EQ & Effects** | 10-band EQ, compressor, reverb with 8 presets |
| 🔌 **Plugin System** | 6 built-in plugins with live parameter control |
| 🎨 **Theme Engine** | 4 built-in themes + custom theme builder |
| 🛠️ **Build Console** | Simulated EXE / APK / macOS / iOS builds |

---

## 🎵 Supported Audio Formats

`FLAC` · `DSD` · `MP3` · `MQA` · `WAV` · `AAC` · `M4A` · `OGG` · `Opus`

---

## 🗂️ Project Structure

```
ProjectSound/
├── app.py                    # Flask server (main entry point)
├── requirements.txt          # Python dependencies
├── run.bat / run.sh          # Platform launchers
│
├── AI/
│   ├── auto_tagging_ai.py    # AI metadata tagger
│   └── noise_filter.py       # Noise reduction module
│
├── Player/
│   └── player_core.py        # Waveform extraction
│
├── PluginLoader/             # Plugin discovery & registry
├── Plugins/                  # reverb, spectrum, EQ, compressor…
│
├── ThemeEngine/              # Theme management
├── ThemeBuilder/themes/      # JSON theme files
│
├── AdminConsole/             # Admin GUI
├── Scripts/                  # Build simulators (EXE, APK, etc.)
│
├── templates/
│   └── index.html            # Single-page frontend
└── static/uploads/           # Uploaded audio files (gitignored)
```

---

## 🔌 Built-in Plugins

1. Reverb
2. Spectrum Analyzer
3. 10-Band Equalizer
4. Compressor
5. *(more coming soon)*

---

## 🎨 Built-in Themes

- Dark Audiophile
- Light Studio
- Neon Night
- Minimal White
- *(+ custom theme builder)*

---

## 📦 Dependencies

Key libraries used (see `requirements.txt` for full list):

- **Flask** — web server & routing
- **mutagen** — audio metadata reading/writing
- **librosa / numpy** — audio processing & waveform analysis

---

## 🛣️ Roadmap

See `Full_Roadmap.txt` for the complete feature roadmap and planned improvements.

---

## 👤 Author

**Navajeevan Panthi**  
GitHub: [@Navajeevanpanthi](https://github.com/Navajeevanpanthi)

---

## 📄 License

This project is currently unlicensed. All rights reserved by the author.
