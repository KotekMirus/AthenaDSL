import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter
from exam_elements_handlers import Exam_Element
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64
import js


def main(user_input: str) -> None:
    whole_text_tokenized: list[list[str]] = tokenizer.segment_text(user_input)
    parsed_document: dict[str, list[list[Exam_Element]]] = parser.parse_document(
        whole_text_tokenized
    )
    font_path: str = "fonts/arial.ttf"
    pdfmetrics.registerFont(TTFont("Arial", font_path))
    pdf: interpreter.PDF_Creator = interpreter.PDF_Creator(
        "TEST.pdf", parsed_document, "Arial"
    )
    pdf.create_empty_pdf()
    pdf.add_to_pdf()
    pdf.save_pdf()
    with open("TEST.pdf", "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
    js.document.setpdfView(base64_encoded)
