import copy
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Circle
from reportlab.lib import colors
import math


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


def create_new_page(
    canvas: canvas, height: float, width: float, margin: float, font: str
) -> float:
    canvas.showPage()
    canvas.setFillColorRGB(1, 1, 1)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColorRGB(0, 0, 0)
    if font:
        canvas.setFont(font, 12)
    current_height = height - margin
    return current_height


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
            current_height = create_new_page(canvas, height, width, margin, font)
        canvas.setFont(font, self.font_size)
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height


class Question(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.words: list[str] = arguments
        self.font_size: int = 13

    def get_height(
        self, width: float, font: str, margin: float, current_question_number: int
    ) -> float:
        words = ["Pytanie", str(current_question_number) + "."] + self.words
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            words, width - 2 * margin, font, self.font_size
        )
        question_height: float = len(lines) * line_spacing
        return question_height

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
        current_question_number: int,
    ) -> float:
        self.words = ["Pytanie", str(current_question_number) + "."] + self.words
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 2 * margin, font, self.font_size
        )
        question_height: float = len(lines) * line_spacing
        if current_height - question_height < margin:
            current_height = create_new_page(canvas, height, width, margin, font)
        canvas.setFont(font, self.font_size)
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height


class Answer(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.words: list[str] = arguments
        self.font_size: int = 12

    @staticmethod
    def get_all_answers_height(
        width: float,
        font: str,
        margin: float,
        chunk_size: int,
        block: list[Exam_Element],
    ) -> tuple[float, int, list[float]]:
        block_copy: list[Exam_Element] = copy.deepcopy(block)
        orientation: int = 0
        answers_count: int = 0
        for exam_element in block_copy:
            if type(exam_element) is Answer:
                answers_count += 1
                if answers_count == 1:
                    if exam_element.words[1] == "_":
                        orientation = 1
                    else:
                        orientation = 0
                if exam_element.words[1] == "|" or exam_element.words[1] == "_":
                    exam_element.words.pop(1)
            else:
                exam_element = None
        answers_list: list[Answer] = [
            item for item in block_copy if type(item) is Answer
        ]
        if orientation == 0:
            # lines_between_answers: float = (len(answers_list) - 1) * 1 * cm
            semi_final_height: float = 0
            line_spacing: float = answers_list[0].font_size * 1.2
            for answer in answers_list:
                lines: list[str] = split_text_to_lines(
                    answer.words,
                    width - 2 * margin,
                    font,
                    answer.font_size,
                )
                semi_final_height += len(lines) * line_spacing
            final_height: float = semi_final_height  # + lines_between_answers
            return final_height, orientation, None
        else:
            line_spacing: float = answers_list[0].font_size * 1.2
            segmented_answers_list: list[list[Answer]] = [
                answers_list[i : i + chunk_size]
                for i in range(0, len(answers_list), chunk_size)
            ]
            gaps_between_answers: float = (chunk_size - 1) * 0.2 * cm
            longest_answers: list[Answer] = []
            rows_heights: list[float] = []
            for segment in segmented_answers_list:
                longest_answer: Answer = None
                longest_answer_lines_number: int = 0
                for answer in segment:
                    answer_lines: list[str] = split_text_to_lines(
                        answer.words,
                        ((width - 2 * margin) / chunk_size) - gaps_between_answers,
                        font,
                        answer.font_size,
                    )
                    if len(answer_lines) > longest_answer_lines_number:
                        longest_answer = answer
                        longest_answer_lines_number = len(answer_lines)
                longest_answers.append(longest_answer)
                rows_heights.append(longest_answer_lines_number * line_spacing)
            line_spacing: float = longest_answers[0].font_size * 1.2
            semi_final_height: float = 0
            for long_answer in longest_answers:
                lines: list[str] = split_text_to_lines(
                    long_answer.words,
                    ((width - 2 * margin) / chunk_size) - gaps_between_answers,
                    font,
                    long_answer.font_size,
                )
                semi_final_height += len(lines) * line_spacing
            lines_between_answers: float = (len(segmented_answers_list) - 1) * 0.15 * cm
            final_height: float = semi_final_height + lines_between_answers
            return final_height, orientation, rows_heights

    def add_to_pdf_vertical(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        if self.words[1] == "|" or self.words[1] == "_":
            self.words.pop(1)
        self.words[0] = self.words[0] + "."
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 2 * margin, font, self.font_size
        )
        answer_height: float = len(lines) * line_spacing
        if current_height - answer_height < margin:
            current_height = create_new_page(canvas, height, width, margin, font)
        canvas.setFont(font, self.font_size)
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height

    def add_to_pdf_horizontal(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
        chunk_size: int,
        current_chunk_position: int,
    ) -> float:
        if self.words[1] == "|" or self.words[1] == "_":
            self.words.pop(1)
        self.words[0] = self.words[0] + "."
        line_spacing: float = self.font_size * 1.2
        gaps_between_answers: float = (chunk_size - 1) * 0.2 * cm
        lines: list[str] = split_text_to_lines(
            self.words,
            ((width - 2 * margin) / chunk_size) - gaps_between_answers,
            font,
            self.font_size,
        )
        canvas.setFont(font, self.font_size)
        for line in lines:
            canvas.drawString(
                margin
                + (((width - 2 * margin) / chunk_size) * current_chunk_position)
                + current_chunk_position * 0.2 * cm,
                current_height,
                line,
            )
            current_height -= line_spacing


class Timeline(Exam_Element):
    def __init__(self, arguments: list[str]):
        from exam_elements_set import options_dictionary

        self.font: str = "Helvetica"
        self.font_size: int = 10

        for argument in arguments:
            if argument in options_dictionary:
                if options_dictionary[argument] == "range":
                    self.range: list[int] = [
                        int(number)
                        for number in arguments[arguments.index(argument) + 1].split(
                            ","
                        )
                    ]
                elif options_dictionary[argument] == "unit":
                    self.unit: int = int(arguments[arguments.index(argument) + 1])

    @staticmethod
    def get_height(width, margin) -> float:
        rect_width: float = (width - 2 * margin) * 0.9
        rect_height: float = rect_width * 0.055
        line_spacing: float = 10 * 1.2
        return rect_height + line_spacing + 0.45 * cm

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        margin: float,
    ) -> float:
        if current_height - Timeline.get_height(width, margin) < margin:
            current_height = create_new_page(canvas, height, width, margin, None)
        current_height -= 0.45 * cm
        rect_width: float = (width - 2 * margin) * 0.9
        rect_height: float = rect_width * 0.055
        triangle_base: float = rect_width * 0.1
        offset: float = (triangle_base - rect_height) / 2
        line_spacing: float = self.font_size * 1.2
        canvas.rect(
            margin,
            current_height - offset,
            rect_width,
            rect_height,
            stroke=1,
            fill=0,
        )
        canvas.line(
            margin + rect_width,
            current_height - 2 * offset,
            margin + rect_width,
            current_height + rect_height,
        )
        canvas.line(
            margin + rect_width,
            current_height - 2 * offset,
            width - margin,
            current_height,
        )
        canvas.line(
            margin + rect_width,
            current_height + rect_height,
            width - margin,
            current_height,
        )
        for position in range(self.unit):
            canvas.line(
                margin + ((rect_width / self.unit) * (position + 1)),
                current_height - offset,
                margin + ((rect_width / self.unit) * (position + 1)),
                current_height - offset + rect_height,
            )
        canvas.setFont(self.font, self.font_size)
        canvas.drawString(margin, current_height - rect_height, str(self.range[0]))
        canvas.drawString(
            (margin + rect_width)
            - (pdfmetrics.stringWidth(str(self.range[1]), self.font, self.font_size)),
            current_height - rect_height,
            str(self.range[1]),
        )
        return current_height - rect_height - line_spacing


class Box(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.gap_between_lines: float = 29
        self.square_side_size: float = 12
        from exam_elements_set import options_dictionary

        for argument in arguments:
            if argument in options_dictionary:
                if options_dictionary[argument] in ["lines", "grid", "empty"]:
                    self.type: str = options_dictionary[argument]
                    self.size: int = int(arguments[arguments.index(argument) + 1])

    def get_height(self) -> float:
        height: float = 0
        if self.type == "lines":
            height = self.size * self.gap_between_lines
        elif self.type == "grid":
            height = (self.size + 1) * self.square_side_size
        elif self.type == "empty":
            height = self.size * self.gap_between_lines
        return height

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        margin: float,
    ) -> float:
        box_height: float = self.get_height()
        if current_height - box_height < margin:
            current_height = create_new_page(canvas, height, width, margin, None)
        if self.type == "lines":
            canvas.setLineWidth(0.4)
            current_height -= 0.5 * self.gap_between_lines
            for _ in range(self.size):
                canvas.line(
                    margin,
                    current_height,
                    width - margin,
                    current_height,
                )
                current_height -= self.gap_between_lines
            current_height += 0.5 * self.gap_between_lines
            canvas.setLineWidth(1)
        elif self.type == "grid":
            canvas.setLineWidth(0.3)
            for _ in range(self.size):
                canvas.line(margin, current_height, width - margin, current_height)
                current_width: float = margin
                while current_width < width - margin:
                    canvas.line(
                        current_width,
                        current_height,
                        current_width,
                        current_height - self.square_side_size,
                    )
                    current_width += self.square_side_size
                current_height -= self.square_side_size
            canvas.line(
                margin,
                current_height,
                width - margin,
                current_height,
            )
            current_height -= self.square_side_size
            canvas.setLineWidth(1)
        elif self.type == "empty":
            for _ in range(self.size):
                current_height -= self.gap_between_lines
        return current_height


class Pie_Chart(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.numbers: list[int] = []
        self.labels: list[str] = []
        label: str = ""
        for argument in arguments:
            if argument[0] == "#":
                if len(self.numbers) > 0:
                    self.labels.append(label)
                    label = ""
                self.numbers.append(int(argument[1:]))
            else:
                if label:
                    label += " " + argument
                else:
                    if argument == "_":
                        label = 7 * "_"
                    elif argument == "|":
                        label = ""
                    else:
                        label = argument
        self.labels.append(label)

    @staticmethod
    def get_height(width: float) -> float:
        return int(0.27 * width)

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        drawing_side_length: int = int(0.27 * width)
        if current_height - drawing_side_length < margin:
            current_height = create_new_page(canvas, height, width, margin, font)
        drawing: Drawing = Drawing(drawing_side_length, drawing_side_length)
        pie_chart: Pie = Pie()
        pie_chart.x = 0
        pie_chart.y = 0
        pie_chart.width = drawing_side_length
        pie_chart.height = drawing_side_length
        pie_chart.data = self.numbers
        pie_chart.labels = self.labels
        pie_chart.sideLabels = True
        for i in range(len(self.numbers)):
            pie_chart.slices[i].fillColor = colors.white
            pie_chart.slices[i].fontName = font
            pie_chart.slices[i].strokeWidth = 1.5
        drawing.add(pie_chart)
        renderPDF.draw(
            drawing,
            canvas,
            width / 2 - drawing_side_length / 2,
            current_height - drawing_side_length,
        )
        line_spacing: float = 12 * 1.2
        return current_height - drawing_side_length - line_spacing


class True_False_Table(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.words: list[str] = arguments
        self.font_size: int = 11

    @staticmethod
    def get_height(
        width: float, margin: float, font: str, block: list[Exam_Element]
    ) -> float:
        block_copy: list[Exam_Element] = copy.deepcopy(block)
        for exam_element in block_copy:
            if type(exam_element) is not True_False_Table:
                exam_element = None
        table_elements_list: list[True_False_Table] = [
            item for item in block_copy if type(item) is True_False_Table
        ]
        line_spacing: float = table_elements_list[0].font_size * 1.2
        table_height: float = 0
        for table_element in table_elements_list:
            lines: list[str] = split_text_to_lines(
                table_element.words, width - 3 * margin, font, table_element.font_size
            )
            sentence_height: float = len(lines) * line_spacing
            table_height += sentence_height + 0.265 * line_spacing
        return table_height

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        canvas.setFont(font, self.font_size)
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 3 * margin, font, self.font_size
        )
        sentence_height: float = len(lines) * line_spacing
        if current_height - sentence_height - 0.265 * line_spacing < margin:
            current_height = create_new_page(canvas, height, width, margin, font)
        canvas.line(
            margin,
            current_height + line_spacing,
            width - margin,
            current_height + line_spacing,
        )
        canvas.line(
            margin,
            current_height + line_spacing,
            margin,
            current_height + line_spacing - sentence_height - 0.265 * line_spacing,
        )
        canvas.line(
            width - 2 * margin,
            current_height + line_spacing,
            width - 2 * margin,
            current_height + line_spacing - sentence_height - 0.265 * line_spacing,
        )
        canvas.line(
            width - 1.5 * margin,
            current_height + line_spacing,
            width - 1.5 * margin,
            current_height + line_spacing - sentence_height - 0.265 * line_spacing,
        )
        canvas.line(
            width - margin,
            current_height + line_spacing,
            width - margin,
            current_height + line_spacing - sentence_height - 0.265 * line_spacing,
        )
        canvas.drawString(width - 2 * margin + 6, current_height, "P")
        canvas.drawString(width - 1.5 * margin + 6, current_height, "F")
        for line in lines:
            canvas.drawString(margin + 2, current_height, line)
            current_height -= line_spacing
        return current_height - 0.265 * line_spacing

    def end_table(
        self, canvas: canvas, width: float, current_height: float, margin: float
    ) -> None:
        line_spacing: float = self.font_size * 1.2
        canvas.line(
            margin,
            current_height + line_spacing,
            width - margin,
            current_height + line_spacing,
        )


class Gaps_To_Fill(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.has_numbers: bool = False
        self.type: str = "content"
        self.words: list[str] = copy.deepcopy(arguments)
        self.font_size_content = 12
        self.font_size_options = 10
        from exam_elements_set import options_dictionary

        for argument in arguments[:2]:
            if argument in options_dictionary:
                if options_dictionary[argument] == "content":
                    self.type = "content"
                    self.words.remove(argument)
                elif options_dictionary[argument] == "options":
                    self.type = "options"
                    self.words.remove(argument)
                elif options_dictionary[argument] == "numeration":
                    self.has_numbers = True
                    self.words.remove(argument)
        if self.type == "content":
            gap_count: int = 1
            for i, word in enumerate(self.words):
                if word.startswith("_") and len(word) < 3:
                    punctuation_mark: str = ""
                    gap_number: str = ""
                    if word[-1] in [".", ",", ";", "?", "!"]:
                        punctuation_mark = word[1]
                    if self.has_numbers:
                        gap_number = str(gap_count)
                    self.words[i] = gap_number + 6 * "_" + punctuation_mark
                    gap_count += 1

        if self.type == "options":
            if "#" in self.words:
                groups: list[list[str]] = []
                current: list[str] = []
                for word in self.words:
                    if word == "#":
                        if current:
                            groups.append(current)
                            current = []
                    else:
                        current.append(word)
                if current:
                    groups.append(current)
                self.words = groups

    @staticmethod
    def get_height(
        width: float, margin: float, font: str, block: list[Exam_Element]
    ) -> float:
        block_copy: list[Exam_Element] = copy.deepcopy(block)
        gaps_to_fill_height: float = 0
        gaps_elements_count: int = 0
        for exam_element in block_copy:
            if type(exam_element) is Gaps_To_Fill:
                if exam_element.type == "content":
                    line_spacing: float = exam_element.font_size_content * 1.2
                    lines: list[str] = split_text_to_lines(
                        exam_element.words,
                        width - 2 * margin,
                        font,
                        exam_element.font_size_content,
                    )
                    gaps_to_fill_height += len(lines) * line_spacing
                elif exam_element.type == "options":
                    if exam_element.has_numbers:
                        line_spacing: float = exam_element.font_size_options * 2
                        gaps_to_fill_height += len(exam_element.words) * line_spacing
                    else:
                        line_spacing: float = exam_element.font_size_options * 2
                        lines: list[str] = split_text_to_lines(
                            exam_element.words,
                            width - 2 * margin,
                            font,
                            exam_element.font_size_content,
                        )
                        gaps_to_fill_height += len(lines) * line_spacing
                gaps_elements_count += 1
        line_spacing: float = 10 * 1
        gaps_to_fill_height += (gaps_elements_count - 1) * line_spacing
        return gaps_to_fill_height

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
        total_gaps_height: float,
        is_first_exercise_part: bool,
    ) -> float:
        if is_first_exercise_part:
            if current_height - total_gaps_height < margin:
                current_height = create_new_page(canvas, height, width, margin, font)
        if self.type == "content":
            canvas.setFont(font, self.font_size_content)
            line_spacing: float = self.font_size_content * 1.2
            lines: list[str] = split_text_to_lines(
                self.words, width - 2 * margin, font, self.font_size_content
            )
            for line in lines:
                canvas.drawString(margin, current_height, line)
                current_height -= line_spacing
        elif self.type == "options":
            canvas.setFont(font, self.font_size_options)
            line_spacing: float = self.font_size_options * 2
            if self.has_numbers:
                for i, line_list in enumerate(self.words):
                    line: str = str(i + 1)
                    for word in line_list:
                        line += 5 * " " + word
                    canvas.drawString(margin, current_height, line)
                    current_height -= line_spacing
            else:
                lines: list[str] = split_text_to_lines(
                    self.words, width - 2 * margin, font, self.font_size_options
                )
                for line in lines:
                    canvas.drawCentredString(width / 2, current_height, line)
                    current_height -= line_spacing
        if is_first_exercise_part:
            line_spacing: float = 10 * 1
            current_height -= line_spacing
        return current_height


class Connections(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.font_size: int = 12
        self.column_number: int = 0
        if arguments[0].isnumeric():
            self.column_number = int(arguments.pop(0))
        self.words: list[str] = arguments

    @staticmethod
    def get_height(
        width: float, margin: float, font: str, block: list[Exam_Element]
    ) -> tuple[float, dict[int : list[float]], int]:
        block_copy: list[Exam_Element] = copy.deepcopy(block)
        column_elements_heights: dict[int : list[float]] = {1: [], 2: []}
        connections_count: int = 0
        font_size: int = 0
        for exam_element in block_copy:
            if type(exam_element) is Connections:
                font_size = exam_element.font_size
                connections_count += 1
                line_spacing: float = exam_element.font_size * 1.2
                lines: list[str] = split_text_to_lines(
                    exam_element.words,
                    width / 2 - 2.5 * margin,
                    font,
                    exam_element.font_size,
                )
                column_elements_heights[exam_element.column_number].append(
                    len(lines) * line_spacing
                )
        final_height: float = 0
        min_elements_per_column: int = min(
            len(column_elements_heights[1]), len(column_elements_heights[2])
        )
        for i in range(min_elements_per_column):
            final_height += max(
                column_elements_heights[1][i], column_elements_heights[2][i]
            )
        column_1_size: int = len(column_elements_heights[1])
        column_2_size: int = len(column_elements_heights[2])
        if column_1_size > column_2_size:
            remaining_elements_count: int = column_1_size - column_2_size
            for i in range(remaining_elements_count):
                final_height += column_elements_heights[1][i + min_elements_per_column]
        elif column_2_size > column_1_size:
            remaining_elements_count: int = column_2_size - column_1_size
            for i in range(remaining_elements_count):
                final_height += column_elements_heights[2][i + min_elements_per_column]
        longest_column_size: int = max(
            len(column_elements_heights[1]), len(column_elements_heights[2])
        )
        for _ in range(longest_column_size):
            final_height += font_size * 0.33
        return final_height, column_elements_heights, connections_count

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        exercise_starting_height: float,
        font: str,
        margin: float,
        column_elements_heights: dict[int : list[float]],
        element_row_number: int,
    ) -> None:
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width / 2 - 2.5 * margin, font, self.font_size
        )
        canvas.setFont(font, self.font_size)
        column_left_side_position: float = margin
        if len(lines) == 1 and self.column_number == 1:
            line_width: float = pdfmetrics.stringWidth(lines[0], font, self.font_size)
            column_left_side_position = width / 2 - 1.5 * margin - line_width - 2
        if self.column_number == 2:
            column_left_side_position: float = width / 2 + 1.5 * margin
        current_height: float = exercise_starting_height
        column_1_size: int = len(column_elements_heights[1])
        column_2_size: int = len(column_elements_heights[2])
        min_elements_per_column: int = min(column_1_size, column_2_size)
        loop_range: int = min(element_row_number, min_elements_per_column - 1)
        for i in range(loop_range):
            current_height -= max(
                column_elements_heights[1][i],
                column_elements_heights[2][i],
            )
        if element_row_number > min_elements_per_column - 1:
            remaining_elements_count: int = element_row_number - loop_range
            longer_column_number: int = 1
            if column_1_size > column_2_size:
                longer_column_number: int = 1
            elif column_2_size > column_1_size:
                longer_column_number: int = 2
            for i in range(remaining_elements_count):
                current_height -= column_elements_heights[longer_column_number][
                    i + loop_range
                ]
        dot_left_side_position: float = (
            width / 2 - 1.5 * margin
            if self.column_number == 1
            else width / 2 + 1.5 * margin - 6 - 2
        )
        current_height -= self.font_size * 0.33 * element_row_number
        for i, line in enumerate(lines):
            if i == math.ceil(len(lines) / 2) - 1:
                drawing = Drawing(6, 6)
                drawing.add(Circle(3, 3, 3, fillColor=colors.black, strokeWidth=0))
                renderPDF.draw(
                    drawing,
                    canvas,
                    dot_left_side_position,
                    current_height,
                )
            canvas.drawString(column_left_side_position, current_height, line)
            current_height -= line_spacing


class Text(Exam_Element):
    def __init__(self, arguments: list[str]):
        self.words: list[str] = arguments
        self.font_size: int = 12

    def get_height(self, width, margin, font) -> float:
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 2 * margin, font, self.font_size
        )
        text_height: float = len(lines) * line_spacing
        return text_height

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        if current_height - self.get_height(width, margin, font) < margin:
            current_height = create_new_page(canvas, height, width, margin, font)
        canvas.setFont(font, self.font_size)
        line_spacing: float = self.font_size * 1.2
        lines: list[str] = split_text_to_lines(
            self.words, width - 2 * margin, font, self.font_size
        )
        for line in lines:
            canvas.drawString(margin, current_height, line)
            current_height -= line_spacing
        return current_height


class Configuration(Exam_Element):
    def __init__(self, arguments: list[str]):
        pass

    def add_to_pdf(
        self,
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
    ) -> float:
        pass


class Exam_Part:
    def __init__(
        self,
        block: list[Exam_Element],
        canvas: canvas,
        height: float,
        width: float,
        current_height: float,
        font: str,
        margin: float,
        current_question_number: int,
    ):
        self.block = block
        self.canvas = canvas
        self.height = height
        self.width = width
        self.current_height = current_height
        self.font = font
        self.margin = margin
        self.current_question_number = current_question_number
        self.chunk_size = 4

    def add_to_pdf(self):
        question = self.block.pop(0)
        question_height: float = question.get_height(
            self.width, self.font, self.margin, self.current_question_number
        )
        exam_element_type_list: list[Exam_Element] = [
            Answer,
            Timeline,
            Box,
            Pie_Chart,
            True_False_Table,
            Gaps_To_Fill,
            Text,
            None,
        ]
        exam_elements_heights: dict[Exam_Element:float] = {
            type_name: 0 for type_name in exam_element_type_list
        }
        timeline_height: float = 0
        answers_height: float = 0
        box_height: float = 0
        pie_chart_height: float = 0
        tf_table_height: float = 0
        gaps_to_fill_height: float = 0
        text_height: float = 0
        connections_height: float = 0
        orientation: int = 0
        rows_heights: list[float] = []
        has_answers: bool = any(type(element) is Answer for element in self.block)
        if has_answers:
            answers_height, orientation, rows_heights = Answer.get_all_answers_height(
                self.width, self.font, self.margin, self.chunk_size, self.block
            )
            exam_elements_heights[Answer] = answers_height
        has_timeline: bool = any(type(element) is Timeline for element in self.block)
        if has_timeline:
            timeline_height = Timeline.get_height(self.width, self.margin)
            exam_elements_heights[Timeline] = timeline_height
        has_box: bool = any(type(element) is Box for element in self.block)
        if has_box:
            found_box_element: Exam_Element = None
            for exam_element in self.block:
                if type(exam_element) is Box:
                    found_box_element = exam_element
                    break
            box_height = found_box_element.get_height()
            exam_elements_heights[Box] = box_height
        has_pie_chart: bool = any(type(element) is Pie_Chart for element in self.block)
        if has_pie_chart:
            pie_chart_height = Pie_Chart.get_height(self.width)
            exam_elements_heights[Pie_Chart] = pie_chart_height
        has_tf_table: bool = any(
            type(element) is True_False_Table for element in self.block
        )
        if has_tf_table:
            tf_table_height = True_False_Table.get_height(
                self.width, self.margin, self.font, self.block
            )
            exam_elements_heights[True_False_Table] = tf_table_height
        has_gaps_to_fill: bool = any(
            type(element) is Gaps_To_Fill for element in self.block
        )
        if has_gaps_to_fill:
            gaps_to_fill_height = Gaps_To_Fill.get_height(
                self.width, self.margin, self.font, self.block
            )
            exam_elements_heights[Gaps_To_Fill] = gaps_to_fill_height
        has_text: bool = any(type(element) is Text for element in self.block)
        if has_text:
            found_text_element: Exam_Element = None
            for exam_element in self.block:
                if type(exam_element) is Text:
                    found_text_element = exam_element
                    break
            text_height = found_text_element.get_height(
                self.width, self.margin, self.font
            )
            exam_elements_heights[Text] = text_height
        all_connections_count: int = 0
        column_elements_heights: dict[int : list[float]] = {}
        has_connections: bool = any(
            type(element) is Connections for element in self.block
        )
        if has_connections:
            connections_height, column_elements_heights, all_connections_count = (
                Connections.get_height(self.width, self.margin, self.font, self.block)
            )
            exam_elements_heights[Connections] = connections_height
        first_exam_element_type: Exam_Element = None
        for exam_element in self.block:
            if exam_element:
                first_exam_element_type = type(exam_element)
                break
        block_height: float = (
            question_height
            + exam_elements_heights[first_exam_element_type]
            + (0.2 * cm)
        )
        if self.current_height - block_height < self.margin:
            self.current_height = create_new_page(
                self.canvas, self.height, self.width, self.margin, self.font
            )
        self.current_height = question.add_to_pdf(
            self.canvas,
            self.height,
            self.width,
            self.current_height,
            self.font,
            self.margin,
            self.current_question_number,
        )
        self.current_height -= 0.2 * cm
        current_horizontal_answer_number: int = 0
        all_answers_count: int = 0
        all_table_elements_count: int = 0
        for exam_element in self.block:
            if type(exam_element) is Answer:
                all_answers_count += 1
            elif type(exam_element) is True_False_Table:
                all_table_elements_count += 1
        added_table_elements_count: int = 0
        first_answer_appearance: bool = True
        first_tf_table_appearance: bool = True
        first_gaps_to_fill_appearance: bool = True
        column_1_connections_count: int = 0
        column_2_connections_count: int = 0
        for exam_element in self.block:
            if type(exam_element) is Answer:
                if first_answer_appearance:
                    if self.current_height - answers_height < self.margin:
                        self.current_height = create_new_page(
                            self.canvas, self.height, self.width, self.margin, self.font
                        )
                    first_answer_appearance = False
                if orientation == 1:
                    if current_horizontal_answer_number % self.chunk_size == 0:
                        if (
                            self.current_height
                            - rows_heights[
                                int(current_horizontal_answer_number / self.chunk_size)
                            ]
                            < self.margin
                        ):
                            self.canvas.showPage()
                            self.canvas.setFillColorRGB(1, 1, 1)
                            self.canvas.rect(
                                0, 0, self.width, self.height, fill=1, stroke=0
                            )
                            self.canvas.setFillColorRGB(0, 0, 0)
                            self.canvas.setFont(self.font, 12)
                            self.current_height = self.height - self.margin
                    exam_element.add_to_pdf_horizontal(
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.margin,
                        self.chunk_size,
                        current_horizontal_answer_number % self.chunk_size,
                    )
                    if (
                        current_horizontal_answer_number % self.chunk_size
                        == self.chunk_size - 1
                        and int((current_horizontal_answer_number + 1) / 4)
                        < len(rows_heights)
                    ):
                        self.current_height -= (
                            rows_heights[int(current_horizontal_answer_number / 4)]
                            + 0.15 * cm
                        )
                    current_horizontal_answer_number += 1
                    if current_horizontal_answer_number == all_answers_count:
                        self.current_height -= rows_heights[-1]
                else:
                    self.current_height = exam_element.add_to_pdf_vertical(
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.margin,
                    )
            elif type(exam_element) is Timeline:
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.margin,
                )
            elif type(exam_element) is Box:
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.margin,
                )
            elif type(exam_element) is Pie_Chart:
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.font,
                    self.margin,
                )
            elif type(exam_element) is True_False_Table:
                if first_tf_table_appearance:
                    if self.current_height - tf_table_height < self.margin:
                        self.current_height = create_new_page(
                            self.canvas, self.height, self.width, self.margin, self.font
                        )
                    first_tf_table_appearance = False
                if added_table_elements_count == 0:
                    self.current_height -= 0.2 * cm
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.font,
                    self.margin,
                )
                added_table_elements_count += 1
                if added_table_elements_count == all_table_elements_count:
                    exam_element.end_table(
                        self.canvas, self.width, self.current_height, self.margin
                    )
            elif type(exam_element) is Gaps_To_Fill:
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.font,
                    self.margin,
                    gaps_to_fill_height,
                    first_gaps_to_fill_appearance,
                )
                first_gaps_to_fill_appearance = False
            elif type(exam_element) is Text:
                self.current_height = exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.font,
                    self.margin,
                )
            elif type(exam_element) is Connections:
                if column_1_connections_count + column_2_connections_count == 0:
                    if self.current_height - connections_height < self.margin:
                        self.current_height = create_new_page(
                            self.canvas, self.height, self.width, self.margin, self.font
                        )
                element_row_number: int = 0
                if exam_element.column_number == 1:
                    element_row_number = column_1_connections_count
                elif exam_element.column_number == 2:
                    element_row_number = column_2_connections_count
                exam_element.add_to_pdf(
                    self.canvas,
                    self.height,
                    self.width,
                    self.current_height,
                    self.font,
                    self.margin,
                    column_elements_heights,
                    element_row_number,
                )
                if exam_element.column_number == 1:
                    column_1_connections_count += 1
                elif exam_element.column_number == 2:
                    column_2_connections_count += 1
                if (
                    column_1_connections_count + column_2_connections_count
                    == all_connections_count
                ):
                    self.current_height -= connections_height
        return self.current_height
