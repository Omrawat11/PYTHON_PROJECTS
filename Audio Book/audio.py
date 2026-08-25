"""
PDF to Audio Book Converter
Extracts text from a PDF file and converts it into an MP3 audio file using pypdf and gTTS.
"""

import argparse
import os
import re
import sys
from io import BytesIO

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pypdf import PdfReader
from gtts import gTTS


def clean_text(text: str) -> str:
    """Clean up extracted PDF text for smoother text-to-speech reading."""
    # Rejoin words broken by hyphens at line endings (e.g., "conver-\nsion" -> "conversion")
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)
    # Replace multiple whitespace characters and newlines with a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from all pages of a PDF file."""
    pdf_path = pdf_path.strip().strip('"').strip("'")
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: '{pdf_path}'")

    text_list = []
    with open(pdf_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        print(f"\n[+] Processing '{os.path.basename(pdf_path)}' ({total_pages} page(s))...")

        for i, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_list.append(page_text.strip())
                else:
                    print(f"  [-] Page {i}: No extractable text (may be an image or scanned page).")
            except Exception as e:
                print(f"  [!] Page {i}: Extraction failed ({e})")

    raw_text = " ".join(text_list)
    cleaned = clean_text(raw_text)

    if not cleaned:
        raise ValueError(
            "No extractable text found in this PDF. It may be empty or contain scanned images only."
        )

    return cleaned


def text_to_speech(text: str, output_path: str, lang: str = "en", slow: bool = False):
    """Convert text to speech and save as an MP3 file."""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    print(f"\n[+] Generating audio (Language: '{lang}', Characters: {len(text)})...")

    # Defensive chunking for large text inputs
    max_chars = 4000
    if len(text) <= max_chars:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_path)
    else:
        words = text.split(" ")
        chunks = []
        current_chunk = []
        current_len = 0

        for word in words:
            if current_len + len(word) + 1 > max_chars:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_len = len(word)
            else:
                current_chunk.append(word)
                current_len += len(word) + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        combined = BytesIO()
        for idx, chunk in enumerate(chunks, start=1):
            print(f"  [*] Synthesizing chunk {idx}/{len(chunks)}...")
            tts = gTTS(text=chunk, lang=lang, slow=slow)
            buf = BytesIO()
            tts.write_to_fp(buf)
            combined.write(buf.getvalue())

        with open(output_path, "wb") as f:
            f.write(combined.getvalue())

    print(f"[✓] Success! Audio file saved to:\n    {os.path.abspath(output_path)}")


def get_interactive_pdf_choice() -> str:
    """Prompt user interactively to select or enter a PDF path."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith(".pdf")]

    print("=" * 60)
    print("           PDF to Audio Book Converter           ")
    print("=" * 60)

    if pdf_files:
        print("\nAvailable PDF file(s) in this folder:")
        for idx, f in enumerate(pdf_files, start=1):
            print(f"  [{idx}] {f}")
        print("  [0] Enter a custom path / drag-and-drop file")

        choice = input(f"\nSelect an option [1-{len(pdf_files)}] or press Enter for [{pdf_files[0]}]: ").strip()
        if choice == "" or choice == "1":
            return os.path.join(current_dir, pdf_files[0])
        elif choice.isdigit() and 1 <= int(choice) <= len(pdf_files):
            return os.path.join(current_dir, pdf_files[int(choice) - 1])

    user_input = input("\nEnter the path to your PDF file: ").strip()
    return user_input.strip('"').strip("'")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF document into an MP3 audiobook using pypdf and gTTS."
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=None,
        help="Path to the input PDF file (optional; prompts interactively if omitted)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output MP3 filename (defaults to <pdf_name>.mp3)",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="en",
        help="Language code (e.g., 'en' for English, 'hi' for Hindi, 'fr' for French, 'es' for Spanish)",
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Speak at a slower speed",
    )
    parser.add_argument(
        "--save-text",
        action="store_true",
        help="Also save extracted text to a .txt file",
    )

    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not pdf_path:
        pdf_path = get_interactive_pdf_choice()

    if not pdf_path:
        print("[!] Error: No PDF path provided. Exiting.")
        sys.exit(1)

    pdf_path = os.path.abspath(pdf_path.strip('"').strip("'"))

    # Determine default output file name
    if args.output:
        output_mp3 = args.output
    else:
        pdf_base = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.dirname(pdf_path)
        output_mp3 = os.path.join(output_dir, f"{pdf_base}.mp3")

    try:
        text = extract_text_from_pdf(pdf_path)
        print(f"[+] Extracted {len(text)} characters.")
        preview = text[:120] + ("..." if len(text) > 120 else "")
        print(f"[+] Preview: \"{preview}\"")

        if args.save_text:
            txt_path = os.path.splitext(output_mp3)[0] + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[+] Text saved to: {txt_path}")

        text_to_speech(text, output_mp3, lang=args.lang, slow=args.slow)

    except Exception as e:
        print(f"\n[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()