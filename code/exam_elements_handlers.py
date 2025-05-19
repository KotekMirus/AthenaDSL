class Exam_Element:
    pass


class Title(Exam_Element):
    def __init__(self, dummy):
        super().__init__()
        self.dummy = dummy

    def __str__(self):
        return self.dummy


class Question(Exam_Element):
    def __init__(self, dummy):
        super().__init__()
        self.dummy = dummy

    def __str__(self):
        return self.dummy


class Answer(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Timeline(Exam_Element):
    def __init__(self, dummy):
        super().__init__()
        self.dummy = dummy

    def __str__(self):
        return self.dummy


class Box(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Pie_Chart(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class True_False_Table(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Connections(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Label_Pictures(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Gaps_To_Fill(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Number_Things(Exam_Element):
    def __init__(self, dummy):
        super().__init__()


class Configuration(Exam_Element):
    def __init__(self, dummy):
        super().__init__()
