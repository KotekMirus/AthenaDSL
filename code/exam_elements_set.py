from exam_elements_handlers import (
    Title,
    Question,
    Answer,
    Timeline,
    Box,
    Pie_Chart,
    True_False_Table,
    Connections,
    Label_Pictures,
    Gaps_To_Fill,
    Number_Things,
    Configuration,
)

blocks_starting_keywords = ["konfiguracja", "tytuł", "pytanie"]

exam_elements_dictionary = {
    "tytuł": Title,
    "pytanie": Question,
    "odpowiedź": Answer,
    "oś_czasu": Timeline,
    "pole": Box,
    "wykres_kołowy": Pie_Chart,
    "prawda_fałsz": True_False_Table,
    "połączenia": Connections,
    "podpisy": Label_Pictures,
    "luki": Gaps_To_Fill,
    "ponumeruj": Number_Things,
    "konfiguracja": Configuration,
}

options_dictionary = {"zakres": "range", "jednostka": "unit"}
