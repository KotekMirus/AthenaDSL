from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm


def split_text_to_lines(words, max_width, font_name, font_size):
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        line_width = pdfmetrics.stringWidth(test_line, font_name, font_size)
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
    def __init__(self, arguments):
        self.words = arguments

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        line_spacing = 16 * 1.2
        lines = split_text_to_lines(self.words, width - 2 * margin, font, 16)
        title_height = len(lines) * line_spacing
        if current_height - title_height < margin:
            canvas.showPage()
            canvas.setFont(font, 16)
            current_height = height - margin
        canvas.setFont(font, 16)
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height


class Question(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        pass


class Answer(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        pass


class Timeline(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        pass


class Box(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, width, current_height, font, margin):
        pass


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
