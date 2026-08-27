<div align="center">

# 🐍 PYTHON_PROJECTS

**A growing collection of Python mini-projects — automation, games, and utilities.**

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

[![GitHub](https://img.shields.io/badge/GitHub-Omrawat11-181717?style=for-the-badge&logo=github)](https://github.com/Omrawat11)

</div>

---

## 📖 About

This repo is where I build and document small, self-contained Python projects while learning — everything from desktop automation and system utilities to simple games. Each project lives in its own folder with its own code (and a dedicated README for the bigger ones).

## 📂 Projects

<table>
<tr>
<th align="left">Project</th>
<th align="left">Description</th>
<th align="left">Tech</th>
<th align="left">Link</th>
</tr>

<tr>
<td>🔋 <b>Battery Notification</b></td>
<td>Real-time Windows battery monitor with low/critical toast alerts, charging detection, and remaining-time estimates.</td>
<td><code>psutil</code>, <code>win10toast</code></td>
<td><a href="./Battery%20Notification">View →</a></td>
</tr>

<tr>
<td>🐢 <b>Turtle Racing</b></td>
<td>A playful turtle-racing game with betting, countdown animation, and replay support, built on Python's <code>turtle</code> module.</td>
<td><code>turtle</code></td>
<td><a href="./Turtle_Racing">View →</a></td>
</tr>

<tr>
<td>🔳 <b>QR Code Generator</b></td>
<td>Generates a QR code image pointing to a URL (currently set to a GitHub profile).</td>
<td><code>qrcode</code></td>
<td><a href="./QR%20Code">View →</a></td>
</tr>

<tr>
<td>🛡️ <b>Captcha Generator</b></td>
<td>Advanced interactive CAPTCHA generator suite with multi-engine rendering (PIL & Captcha library), audio TTS accessibility, multiple challenge modes, and verification analytics.</td>
<td><code>Pillow</code>, <code>captcha</code>, <code>pywin32</code> / <code>tkinter</code></td>
<td><a href="./Captcha%20Generator">View →</a></td>
</tr>

<tr>
<td>🔊 <b>Text to Speech</b></td>
<td>Converts a text string into a spoken MP3 file using Google's TTS engine.</td>
<td><code>gTTS</code></td>
<td><a href="./Text%20to%20speech">View →</a></td>
</tr>

<tr>
<td>✊📄✂️ <b>Rock Paper Scissors</b></td>
<td>Command-line Rock–Paper–Scissors game, first to 5 points wins.</td>
<td>Standard library</td>
<td><a href="./PROJ_1.py">View →</a></td>
</tr>

</table>

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Omrawat11/PYTHON_PROJECTS.git
cd PYTHON_PROJECTS

# Enter a project folder and install its dependencies (if it has a requirements.txt)
cd "Captcha Generator"
pip install -r requirements.txt
python captcha.py
```

Projects without a `requirements.txt` list their dependencies at the top of the main script (e.g. `# pip install qrcode`).

## 🛠️ Tech Stack

| Category | Libraries |
| :--- | :--- |
| System / Automation | `psutil`, `win10toast`, `pywin32` |
| Media / Generation | `qrcode`, `gTTS`, `Pillow`, `captcha` |
| Graphics / Games / GUI | `turtle`, `tkinter` |

## 🗺️ Roadmap

- [x] Battery notification system
- [x] Turtle racing game
- [x] QR code generator
- [x] Text-to-speech demo
- [x] Captcha Generator Studio
- [ ] Add more automation scripts
- [ ] Add a requirements.txt per project consistently
- [ ] Add a shared `utils/` folder for common helpers

## 📄 License

Distributed under the **MIT License**. Individual projects may include their own `LICENSE` file.

<div align="center">
<sub>Made with ❤️ by <a href="https://github.com/Omrawat11">Omrawat11</a></sub>
</div>
