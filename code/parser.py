from typing import Type
import exam_elements_set
from exam_elements_handlers import Exam_Element


def extract_blocks(
    whole_text_tokenized: list[list[list[str], int]],
) -> list[list[list[list[str], int]]]:
    blocks_starting_points: int = []
    blocks: list[list[list[list[str], int]]] = []
    for index, line_and_number in enumerate(whole_text_tokenized):
        line: list[str] = line_and_number[0]
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
    tokenized_line: list[str], line_number: int
) -> tuple[Exam_Element, str] | tuple[None, None]:
    if not tokenized_line:
        return None, None
    command: str = tokenized_line.pop(0).lower()
    class_handler: Type[Exam_Element] = exam_elements_set.exam_elements_dictionary.get(
        command
    )
    exam_element: Exam_Element = None
    if class_handler:
        try:
            exam_element = class_handler(tokenized_line)
        except Exception:
            raise Exception(f"Error in line {line_number}")
    return exam_element, command


def parse_config(
    blocks: list[list[list[list[str], int]]],
) -> tuple[str, dict[str : list[str]]]:
    config_original_name: str = None
    config_dict: dict[str : list[str]] = {}
    for block in blocks:
        if (
            exam_elements_set.config_elements_dictionary.get(block[0][0][0].lower())
            == "configuration"
        ):
            config_original_name = block[0][0][0].lower()
            for line_and_number in block:
                line: list[str] = line_and_number[0]
                config_element: str = exam_elements_set.config_elements_dictionary.get(
                    line[0].lower()
                )
                if config_element:
                    new_line: list[str] = []
                    for word in line[1:]:
                        detected_option = exam_elements_set.options_dictionary.get(word)
                        if detected_option:
                            new_line.append(detected_option)
                        else:
                            new_line.append(word)
                    config_dict[config_element] = new_line
            break
    return config_original_name, config_dict


def parse_document(
    whole_text_tokenized: list[list[list[str], int]],
) -> tuple[dict[str, list[list[list[Exam_Element, int]]]], dict[str : list[str]]]:
    exam_parts: dict[str, list[list[Exam_Element]]] = {
        part_name: [] for part_name in exam_elements_set.blocks_starting_keywords
    }
    blocks: list[list[list[list[str], int]]] = extract_blocks(whole_text_tokenized)
    config_original_name, config_dict = parse_config(blocks)
    for block in blocks:
        block_type: str | None = None
        part_of_exam: list[list[Exam_Element, int]] = []
        for line_and_number in block:
            line: list[str] = line_and_number[0]
            line_number: int = line_and_number[1]
            exam_element, element_name = detect_content_type(line, line_number)
            part_of_exam.append([exam_element, line_number])
            if element_name in exam_elements_set.blocks_starting_keywords:
                block_type = element_name
        if block_type:
            exam_parts[block_type].append(part_of_exam)
    if config_original_name:
        exam_parts.pop(config_original_name)
    return exam_parts, config_dict
