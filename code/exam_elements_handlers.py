from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm


def split_text_to_lines(
    words: list[str], max_width: float, font_name: str, font_size: int
) -> list[str]:
    lines: list[str] = []
    current_line: str = ""
    for word in words:
        test_line: str = f"{current_line} {word}".strip()
        line_width: float = pdfmetrics.stringWidth(test_line, font_name, font_size)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


class Exam_Element:
    pass


class Title(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.words: list[str] = arguments
        self.font_size: int = 16

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 2 * margin, font, self.font_size
        )
        title_height: float = len(lines) * line_spacing
        if current_height - title_height < margin:
            canvas.showPage()
            canvas.setFont(font, self.font_size)
            current_height = height - margin
        canvas.setFont(font, self.font_size)
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height


class Question(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        return 100


class Answer(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        return 100


class Timeline(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        return 100


class Box(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        return 100


class Pie_Chart(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class True_False_Table(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class Connections(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class Label_Pictures(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class Gaps_To_Fill(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class Number_Things(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass


class Configuration(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas):
        pass
