# 🐍 PYTHON_PROJECTS

**A growing collection of Python mini-projects — automation, games, and utilities.**

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](#)

[![GitHub](https://img.shields.io/badge/GitHub-Omrawat11-181717?style=for-the-badge&logo=github)](https://github.com/Omrawat11)

---

## 📖 About

This repo is where I build and document small, self-contained Python projects while learning — from desktop automation and system utilities to text-to-speech tools and simple games. Each project lives in its own folder (or as a single script) so it can be run independently.

## 📂 Projects

| Project | Description | Tech | Link |
| --- | --- | --- | --- |
| 🎧 **Audio Book** | Audiobook-style project that turns text into spoken audio. | — | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Audio%20Book) |
| 🔋 **Battery Notification** | Real-time Windows battery monitor with low/critical toast alerts, charging detection, and remaining-time estimates. | `psutil`, `win10toast` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Battery%20Notification) |
| 🐢 **Turtle Racing** | A playful turtle-racing game with betting, countdown animation, and replay support, built on Python's `turtle` module. | `turtle` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Turtle_Racing) |
| 🔳 **QR Code Generator** | Generates a QR code image pointing to a URL (currently set to a GitHub profile). | `qrcode` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/QR%20Code) |
| 🔊 **Text to Speech** | Converts a text string into a spoken MP3 file using Google's TTS engine. | `gTTS` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Text%20to%20speech) |
| ✊📄✂️ **Rock Paper Scissors** | Command-line Rock–Paper–Scissors game, first to 5 points wins. | Standard library | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/blob/main/Rock_Paper_Scissors.py) |

## 🗂️ Repository Structure

```
PYTHON_PROJECTS/
├── Audio Book/
├── Battery Notification/
├── QR Code/
├── Text to speech/
├── Turtle_Racing/
├── Rock_Paper_Scissors.py
├── .gitignore
└── README.md
```

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Omrawat11/PYTHON_PROJECTS.git
cd PYTHON_PROJECTS

# Enter a project folder and install its dependencies (if it has a requirements.txt)
cd "Battery Notification"
pip install -r requirements.txt
python Battery_Notification.py
```

Projects without a `requirements.txt` list their dependencies at the top of the main script (e.g. `# pip install qrcode`).

To run the single-file game from the repo root:

```bash
python Rock_Paper_Scissors.py
```

## 🛠️ Tech Stack

| Category | Libraries |
| --- | --- |
| System / Automation | `psutil`, `win10toast` |
| Media / Generation | `qrcode`, `gTTS` |
| Graphics / Games | `turtle` |

## 🗺️ Roadmap

- [x] Battery notification system
- [x] Turtle racing game
- [x] QR code generator
- [x] Text-to-speech demo
- [x] Rock Paper Scissors game
- [x] Audio Book project
- [ ] Add more automation scripts
- [ ] Add a `requirements.txt` to every project consistently
- [ ] Add a shared `utils/` folder for common helpers

## 📄 License

Distributed under the **MIT License**. Individual projects may include their own `LICENSE` file.

Made with ❤️ by [Omrawat11](https://github.com/Omrawat11)
