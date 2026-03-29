#!/usr/bin/env python3
"""Generate theme JSON files for Word Cannon.

Reads word dictionaries from assets/data/words.{en,ru}.csv, validates
curated theme word lists, and outputs assets/data/themes.{en,ru}.json.

Usage:
    python scripts/generate_themes.py
"""

import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "data"


def load_dictionary(lang: str) -> dict[str, int]:
    """Load word -> frequency mapping from CSV."""
    path = ASSETS / f"words.{lang}.csv"
    words = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 2:
                words[row[0].lower()] = int(row[1])
    return words


# ── Theme definitions ──────────────────────────────────────────────
# Each theme: (english_name, russian_name, english_words, russian_words)
# Words can appear in multiple themes. Target ~30-50 words per theme.

THEMES = [
    (
        "Animals",
        "Животные",
        [
            "horse", "tiger", "eagle", "bear", "wolf", "snake", "fish", "bird",
            "deer", "lion", "mouse", "rabbit", "shark", "whale", "monkey", "cat",
            "dog", "duck", "fox", "frog", "goat", "hen", "pig", "rat", "bat",
            "cow", "bug", "ant", "bee", "fly", "elk", "ram", "ape", "owl",
            "crab", "worm", "seal", "lamb", "swan", "bull",
        ],
        [
            "лошадь", "тигр", "орел", "медведь", "волк", "змея", "рыба", "птица",
            "олень", "лев", "мышь", "кролик", "акула", "кит", "обезьяна", "кот",
            "собака", "утка", "лиса", "лягушка", "коза", "курица", "свинья", "крыса",
            "корова", "жук", "муравей", "пчела", "муха", "лось", "баран", "сова",
            "краб", "червь", "бык", "конь", "заяц", "паук", "ворон", "голубь",
        ],
    ),
    (
        "Nature",
        "Природа",
        [
            "tree", "river", "mountain", "forest", "lake", "ocean", "field",
            "stone", "flower", "grass", "leaf", "root", "seed", "bush", "sand",
            "rock", "hill", "cave", "island", "valley", "stream", "pond", "mud",
            "dirt", "sky", "star", "moon", "sun", "cloud", "rain", "snow",
            "wind", "storm", "frost", "ice", "fire", "earth", "shore", "wood",
        ],
        [
            "дерево", "река", "гора", "лес", "озеро", "океан", "поле",
            "камень", "цветок", "трава", "лист", "корень", "семя", "куст", "песок",
            "скала", "холм", "пещера", "остров", "долина", "ручей", "пруд", "грязь",
            "небо", "звезда", "луна", "солнце", "облако", "дождь", "снег",
            "ветер", "буря", "мороз", "лед", "огонь", "земля", "берег", "роща",
        ],
    ),
    (
        "Food",
        "Еда",
        [
            "bread", "meat", "cheese", "rice", "soup", "fish", "salt", "sugar",
            "milk", "egg", "cake", "pie", "fruit", "apple", "grape", "lemon",
            "onion", "bean", "corn", "nut", "oil", "honey", "sauce", "cream",
            "butter", "steak", "salad", "toast", "jam", "tea", "wine", "beer",
            "juice", "water", "meal", "dish", "cook", "taste", "bite", "feed",
        ],
        [
            "хлеб", "мясо", "сыр", "рис", "суп", "рыба", "соль", "сахар",
            "молоко", "яйцо", "торт", "пирог", "фрукт", "яблоко", "виноград", "лимон",
            "лук", "орех", "масло", "мед", "соус", "сливки",
            "каша", "салат", "чай", "вино", "пиво",
            "сок", "вода", "блюдо", "повар", "вкус", "кусок", "обед", "ужин",
            "завтрак", "перец", "капуста", "морковь", "картошка",
        ],
    ),
    (
        "Home",
        "Дом",
        [
            "house", "door", "window", "wall", "floor", "roof", "room", "bed",
            "chair", "table", "lamp", "mirror", "bath", "sink", "stair", "key",
            "lock", "fence", "garden", "yard", "couch", "shelf", "desk", "rug",
            "towel", "pillow", "sheet", "closet", "garage", "attic", "porch",
            "tile", "brick", "glass", "pipe", "wire", "nail", "paint", "dust",
        ],
        [
            "дом", "дверь", "окно", "стена", "пол", "крыша", "комната", "кровать",
            "стул", "стол", "лампа", "зеркало", "ванна", "лестница", "ключ",
            "замок", "забор", "сад", "двор", "диван", "полка", "ковер",
            "подушка", "шкаф", "гараж", "чердак",
            "плитка", "кирпич", "стекло", "труба", "гвоздь", "краска", "пыль",
            "кухня", "балкон", "потолок", "порог", "крыльцо", "печь",
        ],
    ),
    (
        "Body",
        "Тело",
        [
            "head", "hand", "heart", "eye", "ear", "nose", "mouth", "arm",
            "leg", "foot", "bone", "skin", "blood", "brain", "face", "neck",
            "chest", "back", "knee", "finger", "tooth", "hair", "lip", "nail",
            "lung", "nerve", "muscle", "palm", "thumb", "jaw", "rib", "hip",
            "shin", "wrist", "vein", "skull", "spine", "gut", "fist", "heel",
        ],
        [
            "голова", "рука", "сердце", "глаз", "ухо", "нос", "рот", "нога",
            "кость", "кожа", "кровь", "мозг", "лицо", "шея",
            "грудь", "спина", "колено", "палец", "зуб", "волос", "губа", "ноготь",
            "легкое", "нерв", "мышца", "ладонь", "череп", "кулак", "пятка",
            "плечо", "живот", "бровь", "лоб", "борода", "щека", "локоть",
            "ребро", "горло", "язык",
        ],
    ),
    (
        "Emotions",
        "Эмоции",
        [
            "love", "hate", "fear", "joy", "anger", "hope", "pride", "shame",
            "grief", "trust", "doubt", "envy", "guilt", "calm", "shock", "worry",
            "pain", "laugh", "smile", "cry", "sigh", "mood", "rage", "peace",
            "happy", "sad", "glad", "sorry", "kind", "warm", "cold", "brave",
            "shy", "hurt", "weak", "bold", "soft", "hard", "sweet", "bitter",
        ],
        [
            "любовь", "страх", "радость", "гнев", "надежда", "гордость", "стыд",
            "горе", "зависть", "вина", "покой", "боль",
            "смех", "улыбка", "крик", "вздох", "ярость", "счастье",
            "грусть", "нежность", "тоска", "обида", "ужас", "злость",
            "печаль", "восторг", "тревога", "скука", "жалость", "досада",
            "ревность", "отчаяние", "смелость", "сочувствие", "раздражение",
        ],
    ),
    (
        "Weather",
        "Погода",
        [
            "rain", "snow", "wind", "storm", "cloud", "sun", "fog", "ice",
            "cold", "warm", "hot", "cool", "wet", "dry", "frost", "hail",
            "thunder", "flood", "heat", "freeze", "mist", "dew", "breeze",
            "sky", "shade", "light", "dark", "dawn", "dusk", "glow",
            "bright", "clear", "gray", "chill", "mild", "harsh", "humid",
        ],
        [
            "дождь", "снег", "ветер", "буря", "облако", "солнце", "туман", "лед",
            "холод", "тепло", "жара", "мороз", "град",
            "гром", "наводнение", "иней", "роса", "бриз",
            "небо", "тень", "свет", "мрак", "рассвет", "закат",
            "молния", "вьюга", "метель", "оттепель", "сырость", "засуха",
            "ливень", "шторм", "ураган", "гроза", "сумерки",
        ],
    ),
    (
        "Colors",
        "Цвета",
        [
            "red", "blue", "green", "white", "black", "gray", "brown", "pink",
            "gold", "silver", "orange", "yellow", "purple", "dark", "light",
            "bright", "pale", "deep", "rich", "dull", "warm", "cool", "shade",
            "tone", "tint", "glow", "fade", "flash", "spark", "shine",
            "color", "paint", "dye", "ink", "stain", "blend", "mix",
        ],
        [
            "красный", "синий", "зеленый", "белый", "черный", "серый", "розовый",
            "золото", "серебро", "желтый", "темный", "светлый",
            "яркий", "бледный", "тусклый", "теплый",
            "оттенок", "тон", "блеск", "сияние", "вспышка", "искра",
            "цвет", "краска", "чернила", "пятно", "смесь",
            "радуга", "рыжий", "алый", "багровый", "лиловый", "бирюза",
            "медь", "бронза", "янтарь",
        ],
    ),
    (
        "Family",
        "Семья",
        [
            "mother", "father", "sister", "brother", "son", "daughter", "wife",
            "husband", "baby", "child", "uncle", "aunt", "cousin", "nephew",
            "niece", "twin", "bride", "groom", "parent", "family", "home",
            "love", "care", "bond", "trust", "name", "birth", "age", "grow",
            "life", "kid", "boy", "girl", "man", "woman", "old", "young",
        ],
        [
            "мать", "отец", "сестра", "брат", "сын", "дочь", "жена",
            "муж", "ребенок", "дядя", "тетя", "племянник",
            "невеста", "жених", "родитель", "семья", "дом",
            "любовь", "забота", "имя", "рождение", "возраст",
            "жизнь", "мальчик", "девочка", "мужчина", "женщина",
            "бабушка", "дедушка", "внук", "внучка", "родня", "свадьба",
            "наследник", "потомок", "предок", "поколение",
        ],
    ),
    (
        "City",
        "Город",
        [
            "street", "road", "bridge", "tower", "store", "shop", "park",
            "church", "school", "bank", "hotel", "market", "square", "train",
            "bus", "car", "taxi", "crowd", "noise", "sign", "light", "block",
            "corner", "cross", "lane", "gate", "bench", "clock", "wall",
            "roof", "floor", "step", "path", "walk", "ride", "stop", "turn",
        ],
        [
            "улица", "дорога", "мост", "башня", "магазин", "парк",
            "церковь", "школа", "банк", "отель", "рынок", "площадь", "поезд",
            "автобус", "машина", "такси", "толпа", "шум", "знак", "свет",
            "угол", "переход", "ворота", "скамейка", "часы", "стена",
            "крыша", "тротуар", "перекресток", "фонарь", "вокзал",
            "метро", "аптека", "кафе", "ресторан", "театр", "музей",
        ],
    ),
    (
        "Work",
        "Работа",
        [
            "work", "boss", "team", "task", "goal", "plan", "deal", "trade",
            "job", "pay", "hire", "fire", "lead", "build", "sell", "buy",
            "earn", "spend", "save", "risk", "gain", "loss", "cost", "price",
            "debt", "loan", "tax", "fund", "stock", "bank", "firm", "staff",
            "skill", "tool", "file", "desk", "note", "sign", "rule", "law",
        ],
        [
            "работа", "начальник", "команда", "задача", "цель", "план", "сделка",
            "должность", "зарплата", "успех", "провал",
            "доход", "расход", "риск", "прибыль", "убыток", "цена",
            "долг", "кредит", "налог", "бюджет", "фирма", "штат",
            "навык", "проект", "отчет", "договор", "офис", "карьера",
            "опыт", "клиент", "партнер", "контракт", "оклад", "премия",
        ],
    ),
    (
        "Music",
        "Музыка",
        [
            "song", "sing", "dance", "band", "drum", "beat", "tone", "note",
            "tune", "sound", "voice", "loud", "soft", "bass", "play", "stage",
            "show", "fan", "hit", "pop", "rock", "jazz", "soul", "folk",
            "rap", "horn", "bell", "string", "piano", "guitar", "rhythm",
            "melody", "choir", "solo", "track", "album", "live", "mix",
        ],
        [
            "песня", "танец", "группа", "барабан", "ритм", "тон", "нота",
            "мелодия", "звук", "голос", "бас", "сцена",
            "концерт", "хор", "соло", "альбом", "аккорд",
            "гитара", "скрипка", "флейта", "труба", "пианино",
            "музыка", "оркестр", "дирижер", "припев", "куплет",
            "композитор", "певец", "слушатель", "микрофон", "динамик",
            "партия", "темп", "лад",
        ],
    ),
    (
        "Sports",
        "Спорт",
        [
            "ball", "goal", "team", "game", "race", "run", "win", "lose",
            "score", "kick", "throw", "catch", "hit", "jump", "swim", "ride",
            "fight", "match", "round", "ring", "net", "court", "field",
            "track", "pool", "gym", "coach", "fan", "prize", "cup", "medal",
            "fast", "strong", "speed", "train", "play", "sport", "club",
        ],
        [
            "мяч", "гол", "команда", "игра", "гонка", "бег", "победа",
            "счет", "удар", "бросок", "прыжок", "плавание",
            "борьба", "матч", "раунд", "ринг", "сетка", "корт", "поле",
            "бассейн", "тренер", "приз", "кубок", "медаль",
            "скорость", "сила", "тренировка", "спорт", "клуб",
            "стадион", "финал", "чемпион", "рекорд", "арена", "турнир",
            "судья", "фол", "пенальти",
        ],
    ),
    (
        "Clothes",
        "Одежда",
        [
            "shirt", "dress", "coat", "hat", "shoe", "boot", "belt", "tie",
            "suit", "vest", "skirt", "jeans", "sock", "glove", "scarf",
            "jacket", "pocket", "button", "zip", "thread", "cloth", "silk",
            "wool", "cotton", "lace", "leather", "fur", "size", "fit",
            "wear", "fold", "hang", "wash", "iron", "style", "fashion",
        ],
        [
            "рубашка", "платье", "пальто", "шапка", "ботинок", "ремень",
            "галстук", "костюм", "жилет", "юбка", "джинсы", "носок", "перчатка",
            "шарф", "куртка", "карман", "пуговица", "ткань", "шелк",
            "шерсть", "хлопок", "кожа", "мех", "размер",
            "одежда", "наряд", "мода", "фасон", "воротник",
            "рукав", "подошва", "каблук", "шуба", "свитер", "майка",
            "штаны", "плащ",
        ],
    ),
    (
        "School",
        "Школа",
        [
            "book", "read", "write", "learn", "teach", "test", "class",
            "grade", "study", "math", "pen", "paper", "page", "word", "text",
            "rule", "line", "mark", "note", "board", "chalk", "desk", "bell",
            "break", "lunch", "map", "globe", "exam", "quiz", "science",
            "history", "lesson", "student", "answer", "question",
        ],
        [
            "книга", "чтение", "письмо", "урок", "класс",
            "оценка", "учеба", "ручка", "бумага", "страница", "слово", "текст",
            "правило", "строка", "доска", "мел", "парта", "звонок",
            "перемена", "обед", "карта", "экзамен",
            "наука", "история", "ученик", "ответ", "вопрос",
            "задание", "тетрадь", "учитель", "директор", "портфель",
            "линейка", "ластик", "циркуль", "глобус", "формула",
        ],
    ),
    (
        "Travel",
        "Путешествия",
        [
            "trip", "road", "map", "plane", "train", "ship", "boat", "car",
            "bus", "bag", "pack", "tent", "camp", "hike", "guide", "hotel",
            "beach", "port", "dock", "bridge", "border", "visa", "ticket",
            "flight", "land", "sea", "coast", "island", "route", "path",
            "mile", "north", "south", "east", "west", "journey", "tour",
        ],
        [
            "поездка", "дорога", "карта", "самолет", "поезд", "корабль", "лодка",
            "машина", "автобус", "сумка", "рюкзак", "палатка", "лагерь",
            "гид", "отель", "пляж", "порт", "мост", "граница", "виза", "билет",
            "рейс", "берег", "остров", "маршрут", "тропа",
            "путь", "север", "юг", "восток", "запад", "турист",
            "вокзал", "аэропорт", "паспорт", "багаж", "экскурсия",
        ],
    ),
    (
        "Water",
        "Вода",
        [
            "water", "river", "lake", "ocean", "sea", "wave", "tide", "rain",
            "drop", "pool", "stream", "flood", "ice", "steam", "fog", "dew",
            "pond", "well", "dam", "shore", "beach", "coast", "island",
            "boat", "ship", "sail", "fish", "swim", "dive", "float", "sink",
            "wet", "flow", "pour", "drink", "splash", "bubble", "creek",
        ],
        [
            "вода", "река", "озеро", "океан", "море", "волна", "прилив", "дождь",
            "капля", "бассейн", "ручей", "наводнение", "лед", "пар", "туман", "роса",
            "пруд", "колодец", "плотина", "берег", "пляж", "побережье", "остров",
            "лодка", "корабль", "парус", "рыба", "поток",
            "родник", "водопад", "болото", "залив", "пролив",
            "глубина", "течение", "русло", "омут",
        ],
    ),
    (
        "War",
        "Война",
        [
            "war", "peace", "army", "fight", "battle", "sword", "shield",
            "gun", "bomb", "tank", "ship", "plane", "camp", "fort", "flag",
            "march", "charge", "attack", "defend", "guard", "spy", "trap",
            "siege", "raid", "fire", "shot", "wound", "blood", "death",
            "hero", "soldier", "enemy", "ally", "chief", "rank", "order",
            "victory", "defeat",
        ],
        [
            "война", "мир", "армия", "битва", "меч", "щит",
            "пушка", "бомба", "танк", "корабль", "лагерь", "крепость", "флаг",
            "марш", "атака", "оборона", "стража", "ловушка",
            "осада", "рейд", "огонь", "выстрел", "рана", "кровь", "смерть",
            "герой", "солдат", "враг", "союзник", "приказ",
            "победа", "поражение", "оружие", "пуля", "сражение",
            "генерал", "полковник", "капитан",
        ],
    ),
    (
        "Money",
        "Деньги",
        [
            "money", "gold", "silver", "coin", "bill", "cash", "bank", "debt",
            "loan", "tax", "pay", "earn", "spend", "save", "buy", "sell",
            "trade", "price", "cost", "rich", "poor", "cheap", "deal", "fund",
            "stock", "bond", "profit", "loss", "wage", "tip", "fee", "fine",
            "rent", "budget", "wealth", "fortune", "value", "worth",
        ],
        [
            "деньги", "золото", "серебро", "монета", "купюра", "наличные", "банк",
            "долг", "кредит", "налог", "зарплата",
            "расход", "покупка", "продажа", "торговля", "цена",
            "богатство", "бедность", "сделка", "бюджет",
            "прибыль", "убыток", "доход", "чаевые", "штраф",
            "аренда", "состояние", "стоимость", "вклад", "процент",
            "инвестиция", "валюта", "рубль", "касса", "кошелек",
        ],
    ),
    (
        "Time",
        "Время",
        [
            "time", "hour", "minute", "second", "day", "night", "week",
            "month", "year", "age", "past", "future", "now", "then", "soon",
            "late", "early", "fast", "slow", "rush", "wait", "pause", "start",
            "end", "begin", "finish", "dawn", "dusk", "noon", "clock",
            "watch", "timer", "date", "season", "spring", "summer", "winter",
        ],
        [
            "время", "час", "минута", "секунда", "день", "ночь", "неделя",
            "месяц", "год", "возраст", "прошлое", "будущее", "сейчас",
            "опоздание", "рассвет", "закат", "полдень", "часы",
            "дата", "сезон", "весна", "лето", "зима", "осень",
            "срок", "период", "эпоха", "мгновение", "вечность",
            "утро", "вечер", "полночь", "столетие", "десятилетие",
            "календарь", "расписание",
        ],
    ),
]


def validate_and_filter(theme_words: list[str], dictionary: dict[str, int]) -> list[str]:
    """Return only words that exist in the dictionary, with length >= 3."""
    valid = []
    for w in theme_words:
        w_lower = w.lower()
        if len(w_lower) >= 3 and w_lower in dictionary:
            valid.append(w_lower)
    return valid


def main():
    en_dict = load_dictionary("en")
    ru_dict = load_dictionary("ru")

    en_themes = []
    ru_themes = []

    print(f"English dictionary: {len(en_dict)} words")
    print(f"Russian dictionary: {len(ru_dict)} words")
    print()

    for en_name, ru_name, en_words, ru_words in THEMES:
        valid_en = validate_and_filter(en_words, en_dict)
        valid_ru = validate_and_filter(ru_words, ru_dict)

        # Report missing words
        missing_en = set(w.lower() for w in en_words if len(w) >= 3) - set(valid_en)
        missing_ru = set(w.lower() for w in ru_words if len(w) >= 3) - set(valid_ru)

        en_freq = sum(en_dict[w] for w in valid_en)
        ru_freq = sum(ru_dict[w] for w in valid_ru)

        print(f"[{en_name} / {ru_name}]")
        print(f"  EN: {len(valid_en)} words, total freq={en_freq}")
        if missing_en:
            print(f"  EN missing: {sorted(missing_en)}")
        print(f"  RU: {len(valid_ru)} words, total freq={ru_freq}")
        if missing_ru:
            print(f"  RU missing: {sorted(missing_ru)}")
        print()

        en_themes.append({"name": en_name, "words": sorted(valid_en)})
        ru_themes.append({"name": ru_name, "words": sorted(valid_ru)})

    # Write JSON files
    en_path = ASSETS / "themes.en.json"
    ru_path = ASSETS / "themes.ru.json"

    with open(en_path, "w", encoding="utf-8") as f:
        json.dump({"themes": en_themes}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {en_path}")

    with open(ru_path, "w", encoding="utf-8") as f:
        json.dump({"themes": ru_themes}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {ru_path}")


if __name__ == "__main__":
    main()
