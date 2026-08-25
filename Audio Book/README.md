# 📚 PDF to Audio Book Converter

A Python application that extracts text from PDF documents and converts it into MP3 audio files using `pypdf` and Google Text-to-Speech (`gTTS`).

---

## ✨ Features

- **📖 PDF Text Extraction**: Extracts text across all pages using `pypdf`.
- **🔊 Natural Speech Synthesis**: Converts text to MP3 audio using `gTTS`.
- **🧹 Smart Text Preprocessing**: Cleans up hyphenated line breaks and normalizes spacing.
- **⚡ Large Document Chunking**: Handles multi-page documents without timing out.
- **🎮 Interactive & CLI Modes**: Run interactively or pass flags via command line.
- **🌍 Multi-Language Support**: Supports multiple languages (English, Hindi, French, Spanish, etc.).

---

## 🚀 Installation

1. Clone the repository (if not already cloned):
   ```bash
   git clone https://github.com/Omrawat11/PYTHON_PROJECTS.git
   cd "PYTHON_PROJECTS/Audio Book"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎧 Usage

### 1. Interactive Mode
Run the script directly and follow the on-screen prompts:
```bash
python audio.py
```

### 2. Command Line Mode
Pass the PDF file path and optional arguments directly:
```bash
# Convert a PDF with default output name (<pdf_name>.mp3)
python audio.py sample.pdf

# Specify a custom output name and also save extracted text to .txt
python audio.py sample.pdf -o my_audiobook.mp3 --save-text

# Convert in another language (e.g., Hindi: 'hi', French: 'fr', Spanish: 'es')
python audio.py hindi_doc.pdf -l hi

# Speak at a slower speed
python audio.py sample.pdf --slow
```

---

## ⚙️ Options

| Argument | Description | Default |
| :--- | :--- | :--- |
| `pdf_path` | Path to the PDF file (optional in interactive mode) | `None` |
| `-o`, `--output` | Output MP3 file path | `<pdf_name>.mp3` |
| `-l`, `--lang` | Language code (e.g., `en`, `hi`, `fr`, `es`) | `en` |
| `--slow` | Speak at a slower speed | `False` |
| `--save-text` | Save extracted text to a `.txt` file | `False` |

---

## 📦 Project Structure

```
Audio Book/
├── audio.py           # Main Python application
├── sample.pdf         # Sample PDF for demonstration
├── sample.txt         # Extracted sample text
├── sample.mp3         # Generated sample audio
├── requirements.txt   # Required Python packages
└── README.md          # Documentation
```
