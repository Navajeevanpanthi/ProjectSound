"""Simulate Windows EXE build via PyInstaller."""
import time

def simulate_exe_build() -> list:
    steps = [
        "🔍 Scanning source files…",
        "📦 Collecting dependencies…",
        "⚙️  Compiling player_core.py…",
        "⚙️  Compiling admin_console_gui.py…",
        "⚙️  Compiling auto_tagging_ai.py…",
        "🔗 Linking modules…",
        "🎨 Embedding theme assets…",
        "🔌 Bundling plugins…",
        "✅ ProjectSound-Windows-x64.exe built successfully!",
        "📁 Output: dist/ProjectSound-Windows-x64.exe  (48.2 MB)",
    ]
    return steps
