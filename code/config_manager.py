from typing import Any


class Configuration:
    def __init__(self, configuration_elements: dict[str : list[str]]) -> None:
        self.color = None
        self.font = None
        self.student_data = None
        self.assign_values(configuration_elements)

    def assign_values(self, config_elements: dict[str : list[str]]) -> None:
        font_path: list[str] = config_elements.get("font")
        if font_path:
            self.font: str = font_path[0]
        color_values: list[str] = config_elements.get("color")
        if color_values:
            if (
                len(color_values) == 1
                and color_values[0][0] == "#"
                and len(color_values[0]) == 7
            ):
                self.color = (
                    int(color_values[0][1:3], 16) / 255,
                    int(color_values[0][3:5], 16) / 255,
                    int(color_values[0][5:7], 16) / 255,
                )
            elif len(color_values) == 3:
                self.color = (
                    int(color_values[0]) / 255,
                    int(color_values[1]) / 255,
                    int(color_values[2]) / 255,
                )
        student_data: list[str] = config_elements.get("student_data")
        if student_data:
            self.student_data = []
            for data_fragment in student_data:
                if data_fragment == "all":
                    self.student_data = ["name", "surname", "class", "date"]
                    break
                elif data_fragment in ["name", "surname", "class", "date"]:
                    self.student_data.append(data_fragment)

    def get_values(self) -> dict[str:Any]:
        return {
            "color": self.color,
            "font": self.font,
            "student_data": self.student_data,
        }
