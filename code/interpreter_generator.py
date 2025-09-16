from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from exam_elements_handlers import (
    Exam_Part,
    Exam_Element,
    Question,
    split_text_to_lines,
)
import exam_elements_set
import random
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
            font_path = "fonts/Nunito-Regular.ttf"
        pdfmetrics.registerFont(TTFont("Font", font_path))
        self.font: str = "Font"
        self.student_data: list[str] = None
        student_data: list[str] = config_custom_values.get("student_data")
        if student_data:
            self.student_data = student_data
        self.rng_seed: str = config_custom_values.get("rng_seed")
        if self.rng_seed:
            random.seed(self.rng_seed)
            question_block_name: str = [
                k
                for k, v in exam_elements_set.exam_elements_dictionary.items()
                if v is Question
            ][0]
            random.shuffle(parsed_document[question_block_name])
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
        if self.student_data:
            self.add_place_for_student_data_to_pdf()
        if self.rng_seed:
            self.add_rng_seed_to_pdf()

    def add_place_for_student_data_to_pdf(self):
        font_size: int = 12
        student_data_words: list[str] = [
            k
            for k, v in exam_elements_set.options_dictionary.items()
            if v in self.student_data
        ]
        counter: int = 0
        final_student_data_line: str = ""
        while True:
            student_data_words_with_space: list[str] = []
            for word in student_data_words:
                student_data_words_with_space.append(word + ":" + (counter * "_"))
            line_after_split: list[str] = split_text_to_lines(
                student_data_words_with_space,
                self.width - 2 * self.margin,
                self.font,
                font_size,
            )
            if len(line_after_split) > 1:
                break
            else:
                final_student_data_line = line_after_split[0]
                counter += 1
        self.canvas.setFont(self.font, font_size)
        self.canvas.drawString(
            self.margin,
            self.current_height + 0.2 * self.margin,
            final_student_data_line,
        )
        line_spacing: float = font_size * 1.2
        self.current_height -= line_spacing + 0.25 * self.margin

    def add_rng_seed_to_pdf(self):
        font_size: int = 10
        line_width: float = pdfmetrics.stringWidth(self.rng_seed, self.font, font_size)
        self.canvas.setFont(self.font, font_size)
        self.canvas.drawString(
            self.width - 0.5 * self.margin - line_width,
            self.height - 0.5 * self.margin,
            str(self.rng_seed),
        )

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
