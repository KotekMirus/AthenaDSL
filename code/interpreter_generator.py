from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from exam_elements_handlers import Exam_Part, Exam_Element, Question, Answer
import exam_elements_set
from typing import Any


class PDF_Creator:
    def __init__(
        self,
        out_path: str,
        parsed_document: dict[str, list[list[Exam_Element]]],
        config_custom_values: dict[str:Any],
    ):
        self.path: str = out_path
        color: tuple[int] = config_custom_values.get("color")
        if not color:
            color = (0, 0, 0)
        self.color: tuple[int] = color
        font_path: str = config_custom_values.get("font")
        if not font_path:
            font_path = "fonts/arial.ttf"
        pdfmetrics.registerFont(TTFont("Font", font_path))
        self.font: str = "Font"
        self.margin: float = 1.5 * cm
        self.parsed_document: dict[str, list[list[Exam_Element]]] = parsed_document
        self.current_question_number: int = 0

    def create_empty_pdf(self):
        self.canvas: canvas = canvas.Canvas(self.path, pagesize=A4)
        self.width, self.height = A4  # 210mm x 297mm or in points: 595 x 842
        self.current_height: float = self.height - self.margin
        self.canvas.setFillColorRGB(1, 1, 1)
        self.canvas.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        self.canvas.setFillColorRGB(*self.color)

    def add_to_pdf(self):
        for keyword in exam_elements_set.blocks_starting_keywords:
            if (
                exam_elements_set.config_elements_dictionary.get(keyword)
                == "configuration"
            ):
                continue
            for keyword_block in self.parsed_document[keyword]:
                if type(keyword_block[0]) is Question:
                    self.current_question_number += 1
                    exam_part = Exam_Part(
                        keyword_block,
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.color,
                        self.margin,
                        self.current_question_number,
                    )
                    self.current_height = exam_part.add_to_pdf()
                else:
                    self.current_height = keyword_block[0].add_to_pdf(
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.color,
                        self.margin,
                    )
                self.current_height -= 0.8 * cm

    def save_pdf(self):
        self.canvas.save()
