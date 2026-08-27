# 🛡️ Advanced CAPTCHA Studio & Generator

An interactive, modern, feature-packed CAPTCHA generation and verification suite built in Python using Tkinter and Pillow (PIL).

---

## ✨ Features

- **🎨 Multi-Engine Rendering**:
  - **Built-in Advanced PIL Engine**: Generates distorted characters, dynamic per-character rotation, sinusoidal wave warps, Bezier interference curves, and noise splatter dots.
  - **ImageCaptcha Library Engine**: Direct integration with the official `captcha` library.
  - **Theme support**: Switch between Light CAPTCHA and Dark CAPTCHA modes.

- **🧩 Multiple Challenge Modes**:
  - **Alphanumeric**: Clean, unconfusable mixed letters and numbers (excluding `0`/`O` and `1`/`l`/`I`).
  - **Numeric Only**: 4-8 digit numeric PIN codes.
  - **Math Challenge**: Arithmetic expressions (e.g. `24 + 18 = ?` -> Answer: `42`).
  - **Words**: English dictionary words with letter distortion.

- **🔊 Audio Accessibility (Text-to-Speech)**:
  - Background audio engine using Windows SAPI / pyttsx3 to read CAPTCHA codes aloud clearly for visually impaired users.

- **📊 Verification Analytics & Gamification**:
  - Live Streak Counter 🔥
  - Total Verified Challenges ✅
  - Accuracy Percentage 🎯

- **⚡ Keyboard Shortcuts & Productivity**:
  - <kbd>Enter</kbd> : Verify answer
  - <kbd>Ctrl</kbd> + <kbd>R</kbd> / <kbd>F5</kbd> : Refresh / Regenerate challenge
  - <kbd>Ctrl</kbd> + <kbd>L</kbd> : Listen to audio CAPTCHA
  - <kbd>Ctrl</kbd> + <kbd>S</kbd> : Save CAPTCHA image as PNG
  - <kbd>Esc</kbd> : Clear text input
  - **Copy to Clipboard**: Quick copy for testing & development.

---

## 🚀 Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python captcha.py
```

---

## 🛠️ Configuration Options
Inside the application UI, you can dynamically configure:
- **Type**: Alphanumeric, Numeric, Math Challenge, Words
- **Difficulty**: Easy, Medium, Hard
- **Length**: 4 to 8 characters
- **Case-Sensitivity**: Toggle case-sensitive matching on or off
- **Noise & Waves**: Toggle security distortion curves and speckle dots
- **Dark CAPTCHA Theme**: Switch between light and dark background rendering
