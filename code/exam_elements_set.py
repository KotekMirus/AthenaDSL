from exam_elements_handlers import (
    Title,
    Question,
    Answer,
    Timeline,
    Box,
    Pie_Chart,
    True_False_Table,
    Connections,
    Gaps_To_Fill,
    Text,
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
    "tabela_pf": True_False_Table,
    "luki": Gaps_To_Fill,
    "połączenia": Connections,
    "tekst": Text,
    "konfiguracja": Configuration,
}

options_dictionary = {
    "zakres": "range",
    "jednostka": "unit",
    "linie": "lines",
    "kratka": "grid",
    "puste": "empty",
    "treść": "content",
    "opcje": "options",
    "numeracja": "numeration",
}
