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
from pathlib import Path
import random
from typing import Any


class PDF_Creator:
    def __init__(
        self,
        out_path: str,
        parsed_document: dict[str, list[list[list[Exam_Element, int]]]],
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
        path: Path = Path(font_path)
        font_name: str = path.stem
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        self.font: str = font_name
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
            groups: list[list[list[list[Exam_Element, int]]]] = []
            current_group: list[list[list[Exam_Element, int]]] = []
            for block in parsed_document[question_block_name]:
                question_obj = block[0][0]
                if question_obj.get_type() == "standard":
                    if current_group:
                        groups.append(current_group)
                    current_group = [block]
                elif question_obj.get_type() == "sub":
                    current_group.append(block)
            if current_group:
                groups.append(current_group)
            random.shuffle(groups)
            shuffled_question_blocks = [b for group in groups for b in group]
            parsed_document[question_block_name] = shuffled_question_blocks
        self.margin: float = 1.5 * cm
        self.parsed_document: dict[str, list[list[list[Exam_Element, int]]]] = (
            parsed_document
        )
        self.current_question_number: int = 0
        self.current_subquestion_number: int = 0

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
        line_number_dict: dict[Exam_Element:int] = {}
        parsed_document_without_numbers: dict[str, list[list[Exam_Element]]] = {}
        for key, outer_list in self.parsed_document.items():
            new_outer: list[list[Exam_Element]] = []
            for inner_list in outer_list:
                new_inner: list[Exam_Element] = []
                for element, number in inner_list:
                    new_inner.append(element)
                    line_number_dict[element] = number
                new_outer.append(new_inner)
            parsed_document_without_numbers[key] = new_outer
        for keyword in exam_elements_set.blocks_starting_keywords:
            if (
                exam_elements_set.config_elements_dictionary.get(keyword)
                == "configuration"
            ):
                continue
            for keyword_block in parsed_document_without_numbers[keyword]:
                if type(keyword_block[0]) is Question:
                    if keyword_block[0].get_type() == "standard":
                        self.current_question_number += 1
                        self.current_subquestion_number = 0
                    elif keyword_block[0].get_type() == "sub":
                        self.current_subquestion_number += 1
                    exam_part = Exam_Part(
                        keyword_block,
                        line_number_dict,
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.color,
                        self.margin,
                        self.current_question_number,
                        self.current_subquestion_number,
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
