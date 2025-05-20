import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter

if __name__ == "__main__":
    file = open("sample_test.txt", encoding="utf-8")
    whole_text_tokenized = tokenizer.segment_text(file.read())
    parsed_document = parser.parse_document(whole_text_tokenized)
    pdf = interpreter.PDF_Creator("TEST.pdf", parsed_document, "Helvetica")
    pdf.create_empty_pdf()
    pdf.add_to_pdf()
    pdf.save_pdf()
