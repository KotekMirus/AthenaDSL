import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def main():
    file = open("sample_test.txt", encoding="utf-8")
    whole_text_tokenized = tokenizer.segment_text(file.read())
    parsed_document = parser.parse_document(whole_text_tokenized)
    font_path = "fonts/arial.ttf"
    pdfmetrics.registerFont(TTFont("Arial", font_path))
    pdf = interpreter.PDF_Creator("TEST.pdf", parsed_document, "Arial")
    pdf.create_empty_pdf()
    pdf.add_to_pdf()
    pdf.save_pdf()


if __name__ == "__main__":
    main()
