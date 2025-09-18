import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter
import config_manager as config
from exam_elements_handlers import Exam_Element
import logging
from typing import Any
import base64
import js


def main(user_input: str) -> None:
    logging.basicConfig(level=logging.ERROR, format="%(message)s")
    whole_text_tokenized: list[list[list[str], int]] = tokenizer.segment_text(
        user_input
    )
    parsed_document: dict[str, list[list[list[Exam_Element, int]]]] = None
    config_dict: dict[str : list[str]] = None
    try:
        parsed_document, config_dict = parser.parse_document(whole_text_tokenized)
        configuration: config.Configuration = config.Configuration(config_dict)
        config_custom_values: dict[str:Any] = configuration.get_values()
        pdf: interpreter.PDF_Creator = interpreter.PDF_Creator(
            "TEST.pdf", parsed_document, config_custom_values
        )
        pdf.create_empty_pdf()
        pdf.add_to_pdf()
        pdf.save_pdf()
        with open("TEST.pdf", "rb") as file:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
        js.document.setpdfView(base64_encoded)
    except Exception as e:
        logging.error(e)
