# 🐍 PYTHON_PROJECTS

**A growing collection of Python mini-projects — automation, games, and utilities.**

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

[![GitHub](https://img.shields.io/badge/GitHub-Omrawat11-181717?style=for-the-badge&logo=github)](https://github.com/Omrawat11)

---

## 📖 About

This repo is where I build and document small, self-contained Python projects while learning — everything from desktop automation and system utilities to simple games. Each project lives in its own folder with its own code (and a dedicated README for the bigger ones).

## 📂 Projects

| Project                      | Description                                                                                                            | Tech                    | Link                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------ | ------------------------------------------------------------------------------------------ |
| 📚 **Audio Book (PDF → Speech)** | Extracts text from a PDF and converts it into a spoken MP3 "audiobook," with chunking for long documents and CLI options. | `pypdf`, `gTTS`          | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Audio%20Book)              |
| 🔋 **Battery Notification**   | Real-time Windows battery monitor with low/critical toast alerts, charging detection, and remaining-time estimates.    | `psutil`, `win10toast`   | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Battery%20Notification)    |
| 🐢 **Turtle Racing**          | A playful turtle-racing game with betting, countdown animation, and replay support, built on Python's `turtle` module. | `turtle`                 | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Turtle_Racing)             |
| 🔳 **QR Code Generator**      | Generates a QR code image pointing to a URL (currently set to a GitHub profile).                                       | `qrcode`                 | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/QR%20Code)                 |
| 🔊 **Text to Speech**         | Converts a text string into a spoken MP3 file using Google's TTS engine.                                               | `gTTS`                   | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Text%20to%20speech)        |
| ✊📄✂️ **Rock Paper Scissors** | Command-line Rock–Paper–Scissors game, first to 5 points wins.                                                         | Standard library         | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/blob/main/Rock_Paper_Scissors.py)    |

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Omrawat11/PYTHON_PROJECTS.git
cd PYTHON_PROJECTS

# Enter a project folder and install its dependencies (if it has a requirements.txt)
cd "Audio Book"
pip install -r requirements.txt
python pdf_to_speech.py mybook.pdf
```

Projects without a `requirements.txt` list their dependencies at the top of the main script (e.g. `# pip install qrcode`).

## 🛠️ Tech Stack

| Category            | Libraries               |
| -------------------- | ------------------------- |
| System / Automation  | `psutil`, `win10toast`    |
| Media / Generation   | `qrcode`, `gTTS`, `pypdf` |
| Graphics / Games     | `turtle`                  |

## 🗺️ Roadmap

- [x] Battery notification system
- [x] Turtle racing game
- [x] QR code generator
- [x] Text-to-speech demo
- [x] PDF-to-audiobook converter
- [ ] Add OCR fallback for scanned PDFs
- [ ] Add more automation scripts
- [ ] Add a requirements.txt per project consistently
- [ ] Add a shared `utils/` folder for common helpers

## 📄 License

Distributed under the **MIT License**. Individual projects may include their own `LICENSE` file.

Made with ❤️ by [Omrawat11](https://github.com/Omrawat11)
