import os
from pathlib import Path

# Support both modern pypdf and PyPDF2 (v3.0+)
try:
    from pypdf import PdfMerger
except ImportError:
    try:
        from PyPDF2 import PdfMerger
    except ImportError:
        from PyPDF2 import PdfFileMerger as PdfMerger  # type: ignore[assignment]


# Base directory of the script for reliable path resolution
BASE_DIR = Path(__file__).resolve().parent


# By appending to the end
def by_appending():
    merger = PdfMerger()
    pdf1_path = BASE_DIR / "samplePdf1.pdf"
    pdf2_path = BASE_DIR / "samplePdf2.pdf"
    output_path = BASE_DIR / "mergedPdf.pdf"

    # Either provide file stream
    with open(pdf1_path, "rb") as f1:
        merger.append(f1)
        # Or direct file path
        merger.append(str(pdf2_path))

        merger.write(str(output_path))
    merger.close()
    print(f"[+] Appending merge successful -> {output_path.name}")


# By inserting after a specified page number
def by_inserting():
    merger = PdfMerger()
    pdf1_path = BASE_DIR / "samplePdf1.pdf"
    pdf2_path = BASE_DIR / "samplePdf2.pdf"
    output_path = BASE_DIR / "mergedPdf1.pdf"

    merger.append(str(pdf1_path))
    # Inserts samplePdf2 before index 0 (at the beginning)
    merger.merge(0, str(pdf2_path))
    merger.write(str(output_path))
    merger.close()
    print(f"[+] Insertion merge successful -> {output_path.name}")


if __name__ == "__main__":
    print("=== Running PDF Merge Utility ===")
    by_appending()
    by_inserting()
    print("=== All PDF merges completed successfully ===")

    