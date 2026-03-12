"""Simulate Android APK build via Buildozer / Kivy."""

def simulate_apk_build() -> list:
    return [
        "🤖 Initialising Android build environment…",
        "📱 Target: Android 12+  (armeabi-v7a, arm64-v8a)",
        "🐍 Cross-compiling Python 3.10 for Android…",
        "📦 Packaging Kivy framework…",
        "⚙️  Compiling JNI bridge…",
        "🔑 Signing APK (debug keystore)…",
        "✅ ProjectSound-Android.apk built successfully!",
        "📁 Output: dist/ProjectSound-Android.apk  (32.7 MB)",
    ]
