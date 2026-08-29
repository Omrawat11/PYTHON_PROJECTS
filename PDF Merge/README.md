# 📑 PDF Merge Utility

A clean and lightweight Python script to merge and combine PDF files using `pypdf` / `PyPDF2`. Demonstrates both sequential appending and custom-position page insertion.

---

## ✨ Features

- **➕ Append Mode**: Combines multiple PDF files sequentially into a single document.
- **📍 Insert Mode**: Inserts pages from one PDF into specific page positions of another.
- **🔄 Universal Compatibility**: Works seamlessly with modern `pypdf` as well as `PyPDF2` (v3.0+).
- **🛡️ Safe Resource Management**: Ensures all opened file streams and merger handlers are properly closed after operations.
- **📂 Relative Path Support**: Resolves input/output file paths reliably regardless of current working directory.

---

## 🚀 Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage

Run the script directly:
```bash
python merge.py
```

### Methods Explained

#### 1. By Appending (`by_appending`)
Appends PDF files sequentially in the order they are added.
```python
merger = PdfMerger()
with open("samplePdf1.pdf", "rb") as f1:
    merger.append(f1)
    merger.append("samplePdf2.pdf")
    merger.write("mergedPdf.pdf")
merger.close()
```

#### 2. By Inserting (`by_inserting`)
Inserts a PDF at a specific page index (e.g. index `0` for inserting before the first page).
```python
merger = PdfMerger()
merger.append("samplePdf1.pdf")
merger.merge(0, "samplePdf2.pdf")
merger.write("mergedPdf1.pdf")
merger.close()
```

---

## 📦 Project Structure

```
PDF Merge/
├── merge.py           # Main merge script
├── samplePdf1.pdf     # Sample PDF 1
├── samplePdf2.pdf     # Sample PDF 2
├── mergedPdf.pdf      # Output from sequential appending
├── mergedPdf1.pdf     # Output from custom insertion
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```
