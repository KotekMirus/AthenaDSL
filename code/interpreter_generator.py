from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from exam_elements_handlers import Exam_Part, Exam_Element, Question, Answer
import exam_elements_set


class PDF_Creator:
    def __init__(
        self,
        out_path: str,
        parsed_document: dict[str, list[list[Exam_Element]]],
        font: str,
    ):
        self.path: str = out_path
        self.font: str = font
        self.margin: float = 1.5 * cm
        self.parsed_document: dict[str, list[list[Exam_Element]]] = parsed_document
        self.current_question_number: int = 0

    def create_empty_pdf(self):
        self.canvas: canvas = canvas.Canvas(self.path, pagesize=A4)
        self.width, self.height = A4  # 210mm x 297mm or in points: 595 x 842
        self.current_height: float = self.height - self.margin

    def add_to_pdf(self):
        for keyword in exam_elements_set.blocks_starting_keywords:
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
                        self.margin,
                    )
                self.current_height -= 0.8 * cm

    def save_pdf(self):
        self.canvas.save()
