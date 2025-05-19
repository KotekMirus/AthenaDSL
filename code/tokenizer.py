def segment_text(text: str) -> list[list[str]]:
    lines = [element for element in text.split("\n")]
    words = [element.split() for element in lines]
    return words
