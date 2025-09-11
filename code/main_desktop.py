import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter
import sys
from exam_elements_handlers import Exam_Element
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from typing import IO


def main(filename: str) -> None:
    file_path: Path = Path(filename).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    file: IO[str] = open(file_path, encoding="utf-8")
    whole_text_tokenized: list[list[str]] = tokenizer.segment_text(file.read())
    parsed_document: dict[str, list[list[Exam_Element]]] = parser.parse_document(
        whole_text_tokenized
    )
    font_path: str = "fonts/arial.ttf"
    pdfmetrics.registerFont(TTFont("Arial", font_path))
    output_path: Path = file_path.with_suffix(".pdf")
    pdf: interpreter.PDF_Creator = interpreter.PDF_Creator(
        str(output_path), parsed_document, "Arial"
    )
    pdf.create_empty_pdf()
    pdf.add_to_pdf()
    pdf.save_pdf()


if __name__ == "__main__":
    filename: str = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Please enter filename: ")
    main(filename)
