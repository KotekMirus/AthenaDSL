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
)
from config_manager import Configuration

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
}

config_elements_dictionary = {
    "konfiguracja": "configuration",
    "kolor": "color",
    "czcionka": "font",
    "dane_ucznia": "student_data",
    "losowa_kolejność_pytań": "random_question_order",
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
    "imię": "name",
    "nazwisko": "surname",
    "data": "date",
    "klasa": "class",
    "wszystkie": "all",
    "podpunkt": "subquestion",
}
