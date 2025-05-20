from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from exam_elements_handlers import Exam_Element
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

    def create_empty_pdf(self):
        self.canvas: canvas = canvas.Canvas(self.path, pagesize=A4)
        self.width, self.height = A4  # 210mm x 297mm or in points: 595 x 842
        self.current_height: float = self.height - self.margin

    def add_to_pdf(self):
        for keyword in exam_elements_set.blocks_starting_keywords:
            for keyword_block in self.parsed_document[keyword]:
                for exam_element in keyword_block:
                    if exam_element:
                        self.current_height = exam_element.add_to_pdf(
                            self.canvas,
                            self.height,
                            self.width,
                            self.current_height,
                            self.font,
                            self.margin,
                        )
                        self.current_height -= 1 * cm

    def save_pdf(self):
        self.canvas.save()
