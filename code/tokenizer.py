def segment_text(text: str) -> list[list[list[str], int]]:
    lines = [element for element in text.split("\n")]
    words = [element.split() for element in lines]
    words_and_line_numbers = [[sublist, i + 1] for i, sublist in enumerate(words)]
    return words_and_line_numbers
