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


def parse_config(blocks: list[list[list[str]]]) -> tuple[str, dict[str : list[str]]]:
    config_original_name: str = None
    config_dict: dict[str : list[str]] = {}
    for block in blocks:
        if (
            exam_elements_set.config_elements_dictionary.get(block[0][0])
            == "configuration"
        ):
            config_original_name = block[0][0]
            for line in block:
                config_element: str = exam_elements_set.config_elements_dictionary.get(
                    line[0]
                )
                if config_element:
                    config_dict[config_element] = line[1:]
            break
    return config_original_name, config_dict


def parse_document(
    whole_text_tokenized: list[list[str]],
) -> tuple[dict[str, list[list[Exam_Element]]], dict[str : list[str]]]:
    exam_parts: dict[str, list[list[Exam_Element]]] = {
        part_name: [] for part_name in exam_elements_set.blocks_starting_keywords
    }
    blocks: list[list[list[str]]] = extract_blocks(whole_text_tokenized)
    config_original_name, config_dict = parse_config(blocks)
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
    if config_original_name:
        exam_parts.pop(config_original_name)
    return exam_parts, config_dict
