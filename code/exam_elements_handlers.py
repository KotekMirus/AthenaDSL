from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


class Exam_Element:
    pass


class Title(Exam_Element):
    def __init__(self, arguments):
        self.title = ""
        for a in arguments:
            self.title += " " + a

    def add_to_pdf(self, canvas, height, current_height):
        canvas.drawString(2 * cm, current_height, self.title)


class Question(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, current_height):
        pass


class Answer(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, current_height):
        pass


class Timeline(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, current_height):
        pass


class Box(Exam_Element):
    def __init__(self, dummy):
        pass

    def add_to_pdf(self, canvas, height, current_height):
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
