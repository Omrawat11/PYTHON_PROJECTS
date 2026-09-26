<div align="center">

# 🐍 PYTHON_PROJECTS

**A growing collection of Python mini-projects — automation, games, and utilities.**

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](#)
[![GitHub](https://img.shields.io/badge/GitHub-Omrawat11-181717?style=for-the-badge&logo=github)](https://github.com/Omrawat11)

<sub>⭐ If you find something useful here, consider starring the repo — it helps a lot.</sub>

</div>

---

## 📖 About

This repo is where I build and document small, self-contained Python projects while learning — from desktop automation and system utilities to text-to-speech tools and simple games.

Each project lives in its own folder (or as a single script) so it can be cloned, run, and understood independently — no need to touch the rest of the repo.

> 💡 **New here?** Jump straight to [Quick Start](#-quick-start) to get any project running in under a minute.

---

## 📑 Table of Contents

- [Projects](#-projects)
- [Repository Structure](#️-repository-structure)
- [Quick Start](#-quick-start)
- [Tech Stack](#️-tech-stack)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Connect](#-connect)

---

## 📂 Projects

<details open>
<summary><b>🎧 Audio Book</b> — turns text into spoken audio</summary>

<br>

Audiobook-style project that converts written text into narrated audio, for quick listen-along versions of text content.

| | |
|---|---|
| **Tech** | Python |
| **Run it** | `python audio_book.py` (see folder for the exact entry file) |
| **Link** | [Open folder →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Audio%20Book) |

</details>

<details>
<summary><b>🔋 Battery Notification</b> — real-time Windows battery monitor</summary>

<br>

Watches your battery in the background and pops native toast alerts for low/critical charge, detects when charging starts, and estimates time remaining.

| | |
|---|---|
| **Tech** | `psutil`, `win10toast` |
| **Run it** | `pip install -r requirements.txt` → `python Battery_Notification.py` |
| **Link** | [Open folder →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Battery%20Notification) |

</details>

<details>
<summary><b>🐢 Turtle Racing</b> — a playful betting/racing game</summary>

<br>

A turtle-racing game built on Python's `turtle` module, complete with betting, a countdown animation, and replay support.

| | |
|---|---|
| **Tech** | `turtle` (standard library) |
| **Run it** | `python turtle_racing.py` (see folder for the exact entry file) |
| **Link** | [Open folder →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Turtle_Racing) |

</details>

<details>
<summary><b>🔳 QR Code Generator</b> — text/URL → scannable QR image</summary>

<br>

Generates a QR code image pointing to a URL (currently set to a GitHub profile) — swap the target URL to point anywhere you like.

| | |
|---|---|
| **Tech** | `qrcode` |
| **Run it** | `pip install qrcode` → `python qr_code.py` |
| **Link** | [Open folder →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/QR%20Code) |

</details>

<details>
<summary><b>🔊 Text to Speech</b> — text string → spoken MP3</summary>

<br>

Converts any text string into a spoken MP3 file using Google's TTS engine.

| | |
|---|---|
| **Tech** | `gTTS` |
| **Run it** | `pip install gTTS` → `python text_to_speech.py` |
| **Link** | [Open folder →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Text%20to%20speech) |

</details>

<details>
<summary><b>✊📄✂️ Rock Paper Scissors</b> — classic CLI game, first to 5</summary>

<br>

Command-line Rock–Paper–Scissors against the computer. First player to 5 points wins.

| | |
|---|---|
| **Tech** | Standard library |
| **Run it** | `python Rock_Paper_Scissors.py` |
| **Link** | [Open file →](https://github.com/Omrawat11/PYTHON_PROJECTS/blob/main/Rock_Paper_Scissors.py) |

</details>

<br>

<div align="center">

| Project | Description | Tech | Link |
|---|---|---|---|
| 🎧 **Audio Book** | Turns text into spoken audio | — | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Audio%20Book) |
| 🔋 **Battery Notification** | Battery monitor with toast alerts | `psutil`, `win10toast` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Battery%20Notification) |
| 🐢 **Turtle Racing** | Betting-based turtle race game | `turtle` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Turtle_Racing) |
| 🔳 **QR Code Generator** | URL → QR code image | `qrcode` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/QR%20Code) |
| 🔊 **Text to Speech** | Text → spoken MP3 | `gTTS` | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/tree/main/Text%20to%20speech) |
| ✊📄✂️ **Rock Paper Scissors** | CLI game, first to 5 | Standard library | [View →](https://github.com/Omrawat11/PYTHON_PROJECTS/blob/main/Rock_Paper_Scissors.py) |

</div>

---

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

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Omrawat11/PYTHON_PROJECTS.git
cd PYTHON_PROJECTS

# 2. Enter a project folder and install its dependencies (if it has a requirements.txt)
cd "Battery Notification"
pip install -r requirements.txt
python Battery_Notification.py
```

Projects without a `requirements.txt` list their dependencies at the top of the main script (e.g. `# pip install qrcode`).

To run the single-file game from the repo root:

```bash
python Rock_Paper_Scissors.py
```

---

## 🛠️ Tech Stack

<div align="center">

| Category | Libraries |
|---|---|
| System / Automation | `psutil`, `win10toast` |
| Media / Generation | `qrcode`, `gTTS` |
| Graphics / Games | `turtle` |

</div>

---

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
- [ ] Add short usage GIFs/screenshots per project

---

## 🤝 Contributing

This is primarily a personal learning repo, but suggestions and fixes are welcome:

1. Fork the repo
2. Create a branch (`git checkout -b feature/your-idea`)
3. Commit your changes (`git commit -m "Add: your idea"`)
4. Push and open a Pull Request

Bug reports and small improvements (typos, cleaner code, a missing `requirements.txt`) are especially appreciated.

---

## 📄 License

Distributed under the **MIT License**. Individual projects may include their own `LICENSE` file.

---

## 📬 Connect

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Omrawat11-181717?style=for-the-badge&logo=github)](https://github.com/Omrawat11)

**Made with ❤️ by [Omrawat11](https://github.com/Omrawat11)**

</div>
