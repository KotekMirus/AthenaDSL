import tokenizer as tokenizer
import parser as parser
import interpreter_generator as interpreter
import config_manager as config
import sys
from exam_elements_handlers import Exam_Element
from pathlib import Path
import logging
from typing import IO, Any


def main(filename: str) -> None:
    logging.basicConfig(level=logging.ERROR, format="%(message)s")
    file_path: Path = Path(filename).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    file: IO[str] = open(file_path, encoding="utf-8")
    whole_text_tokenized: list[list[list[str], int]] = tokenizer.segment_text(
        file.read()
    )
    parsed_document: dict[str, list[list[list[Exam_Element, int]]]] = None
    config_dict: dict[str : list[str]] = None
    try:
        parsed_document, config_dict = parser.parse_document(whole_text_tokenized)
        configuration: config.Configuration = config.Configuration(config_dict)
        config_custom_values: dict[str:Any] = configuration.get_values()
        output_path: Path = file_path.with_suffix(".pdf")
        pdf: interpreter.PDF_Creator = interpreter.PDF_Creator(
            str(output_path), parsed_document, config_custom_values
        )
        pdf.create_empty_pdf()
        pdf.add_to_pdf()
        pdf.save_pdf()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    filename: str = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Please enter filename: ")
    main(filename)
