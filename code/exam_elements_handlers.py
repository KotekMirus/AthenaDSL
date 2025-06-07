import copy
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
            canvas.showPage()
            canvas.setFont(font, self.font_size)
            current_height = height - margin
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
    ) -> float:
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
        answers_list: list[Answer] = [item for item in block_copy if item is not None]
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
            canvas.showPage()
            canvas.setFont(font, self.font_size)
            current_height = height - margin
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
        return 90


class Box(Exam_Element):
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
        return 90


class Pie_Chart(Exam_Element):
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


class True_False_Table(Exam_Element):
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


class Connections(Exam_Element):
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


class Label_Pictures(Exam_Element):
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


class Gaps_To_Fill(Exam_Element):
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


class Number_Things(Exam_Element):
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
        answers_height, orientation, rows_heights = Answer.get_all_answers_height(
            self.width, self.font, self.margin, self.chunk_size, self.block
        )
        block_height: float = question_height + answers_height + (0.2 * cm)
        if self.current_height - block_height < self.margin:
            self.canvas.showPage()
            self.canvas.setFont(self.font, 12)
            self.current_height = self.height - self.margin
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
        for exam_element in self.block:
            if type(exam_element) is Answer:
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
                    if current_horizontal_answer_number % self.chunk_size == 3 and int(
                        (current_horizontal_answer_number + 1) / 4
                    ) < len(rows_heights):
                        self.current_height -= (
                            rows_heights[int(current_horizontal_answer_number / 4)]
                            + 0.15 * cm
                        )
                    current_horizontal_answer_number += 1
                else:
                    self.current_height = exam_element.add_to_pdf_vertical(
                        self.canvas,
                        self.height,
                        self.width,
                        self.current_height,
                        self.font,
                        self.margin,
                    )
        return self.current_height
