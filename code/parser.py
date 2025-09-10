from typing import Type
import exam_elements_set
from exam_elements_handlers import Exam_Element


def extract_blocks(whole_text_tokenized: list[list[str]]) -> list[list[list[str]]]:
    blocks_starting_points: int = []
    blocks: list[list[list[str]]] = []
    for index, line in enumerate(whole_text_tokenized):
        if not line:
            continue
        command: str = line[0].lower()
        if command in exam_elements_set.blocks_starting_keywords:
            blocks_starting_points.append(index)
    for i in range(len(blocks_starting_points)):
        start = blocks_starting_points[i]
        end = (
            blocks_starting_points[i + 1]
            if i + 1 < len(blocks_starting_points)
            else len(whole_text_tokenized)
        )
        blocks.append(whole_text_tokenized[start:end])
    return blocks


def detect_content_type(
    tokenized_line: list[str],
) -> tuple[Exam_Element, str] | tuple[None, None]:
    if not tokenized_line:
        return None, None
    command: str = tokenized_line.pop(0).lower()
    class_handler: Type[Exam_Element] = exam_elements_set.exam_elements_dictionary.get(
        command
    )
    exam_element: Exam_Element = None
    if class_handler:
        exam_element = class_handler(tokenized_line)
    return exam_element, command


def parse_document(
    whole_text_tokenized: list[list[str]],
) -> dict[str, list[list[Exam_Element]]]:
    exam_parts: dict[str, list[list[Exam_Element]]] = {
        part_name: [] for part_name in exam_elements_set.blocks_starting_keywords
    }
    blocks: list[list[list[str]]] = extract_blocks(whole_text_tokenized)
    for block in blocks:
        block_type: str | None = None
        part_of_exam: list[Exam_Element] = []
        for line in block:
            exam_element, element_name = detect_content_type(line)
            part_of_exam.append(exam_element)
            if element_name in exam_elements_set.blocks_starting_keywords:
                block_type = element_name
        if block_type:
            exam_parts[block_type].append(part_of_exam)
    return exam_parts
