#!/usr/bin/env python3
"""Generate theme JSON files for Word Cannon.

Reads word dictionaries from assets/data/words.{en,ru}.csv, validates
curated theme word lists (lemmas only), and outputs assets/data/themes.{en,ru}.json.

Each theme targets 100+ validated lemmas per language.
Themes that can't reach 100 in both languages are removed.

Usage:
    python scripts/generate_themes.py
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "data"
MIN_WORDS_PER_THEME = 100


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


def validate_and_filter(theme_words: list[str], dictionary: dict[str, int]) -> list[str]:
    """Return only unique words that exist in the dictionary, with length >= 3."""
    seen = set()
    valid = []
    for w in theme_words:
        w_lower = w.lower()
        if len(w_lower) >= 3 and w_lower in dictionary and w_lower not in seen:
            valid.append(w_lower)
            seen.add(w_lower)
    return valid


# ── Theme definitions ──────────────────────────────────────────────
# Each theme: (english_name, russian_name, english_words, russian_words)
# Only lemmas (base dictionary forms). No inflected/derived forms.
# Words can appear in multiple themes. Target 100+ validated per language.
# Themes are broadly defined to hit the target in English (6.5K word dictionary).

THEMES = [
    (
        "Nature & Animals",
        "Природа и животные",
        [
            # Animals
            "horse", "tiger", "eagle", "bear", "wolf", "snake", "fish", "bird",
            "deer", "lion", "mouse", "rabbit", "shark", "whale", "monkey", "cat",
            "dog", "duck", "fox", "frog", "goat", "pig", "rat", "bat",
            "cow", "bug", "ant", "bee", "fly", "ram", "owl",
            "crab", "worm", "seal", "lamb", "swan", "bull", "pet",
            "chicken", "turkey", "salmon", "donkey", "pigeon",
            "spider", "turtle", "dragon", "monster",
            # Nature
            "tree", "river", "mountain", "forest", "lake", "ocean", "field",
            "stone", "flower", "grass", "leaf", "root", "seed", "bush", "sand",
            "rock", "hill", "cave", "island", "valley", "stream", "pond", "mud",
            "dirt", "sky", "star", "moon", "sun", "cloud", "rain", "snow",
            "wind", "storm", "frost", "ice", "fire", "earth", "shore", "wood",
            "branch", "bark", "vine", "bloom", "grow", "plant", "soil",
            "cliff", "peak", "ridge", "plain", "marsh", "swamp",
            "desert", "jungle", "trail", "path", "creek",
            "spring", "autumn", "winter", "summer", "season", "nature",
            "garden", "park", "wild", "green", "fresh", "deep", "wide", "tall",
            "dry", "wet", "cold", "warm", "hot", "cool", "dark", "bright",
            "sunrise", "sunset", "rainbow", "thunder", "lightning",
            "horizon", "landscape", "crystal", "flood",
            "shade", "dawn", "glow", "fog", "harvest", "oak", "pine",
            "rose", "dust", "ash",
            # Animal actions & body parts
            "tail", "wing", "horn", "fur", "hunt", "trap", "cage",
            "nest", "feed", "breed", "bite", "herd", "pack",
            "prey", "flock", "crawl", "swim", "run", "jump", "hide",
            "chase", "catch", "tame", "ride", "farm", "zoo",
            "bone", "meat", "skin", "milk", "egg", "wool", "leather",
            "feather", "scale", "tooth", "puppy", "beast", "creature", "animal",
        ],
        [
            # Животные
            "лошадь", "тигр", "орел", "медведь", "волк", "змея", "рыба", "птица",
            "олень", "лев", "мышь", "кролик", "кот", "заяц", "паук", "ворон",
            "собака", "утка", "лиса", "коза", "курица", "свинья", "крыса",
            "корова", "жук", "муха", "лось", "баран", "бык", "конь", "голубь",
            "черепаха", "дракон", "обезьяна", "кошка", "скот", "слон",
            "белка", "кабан", "гусь", "петух", "щенок", "котенок",
            "сокол", "ястреб", "воробей", "журавль", "аист",
            "сорока", "синица", "бабочка", "комар", "стрекоза",
            # Природа
            "дерево", "река", "гора", "лес", "озеро", "океан", "поле",
            "камень", "цветок", "трава", "лист", "корень", "семя", "куст", "песок",
            "скала", "холм", "пещера", "остров", "долина", "ручей", "пруд", "грязь",
            "небо", "звезда", "луна", "солнце", "облако", "дождь", "снег",
            "ветер", "буря", "мороз", "лед", "огонь", "земля", "берег", "роща",
            "ветка", "почва", "вершина", "склон", "равнина", "болото",
            "пустыня", "луг", "тропа", "весна", "осень", "зима", "лето",
            "природа", "сад", "парк", "степь", "тайга", "тундра",
            "поляна", "овраг", "родник", "утес",
            "рассвет", "закат", "радуга", "гром", "молния",
            "горизонт", "пейзаж", "тень", "туман", "урожай", "дуб", "сосна",
            "роза", "пыль", "пепел",
            # Части тела животных и действия
            "хвост", "крыло", "рог", "мех", "охота", "ловушка", "клетка",
            "гнездо", "стая", "след", "нора",
            "пастух", "охотник", "зверь", "хищник", "добыча",
            "шкура", "перо", "зуб", "кость", "лапа",
        ],
    ),
    (
        "Home & Food",
        "Дом и еда",
        [
            # Home
            "house", "door", "window", "wall", "floor", "roof", "room", "bed",
            "chair", "table", "lamp", "mirror", "bath", "sink", "key",
            "lock", "fence", "garden", "yard", "couch", "shelf", "desk", "rug",
            "towel", "pillow", "sheet", "closet", "garage", "attic", "porch",
            "brick", "glass", "pipe", "wire", "nail", "paint", "dust",
            "clean", "wash", "sweep", "fix", "build", "move",
            "open", "close", "shut", "hang", "fold", "store",
            "kitchen", "bedroom", "bathroom", "hallway", "basement",
            "ceiling", "carpet", "curtain", "blanket", "mattress",
            "drawer", "cabinet", "counter", "shower", "toilet",
            "light", "switch", "plug", "ladder", "hammer", "screw",
            "bolt", "drill", "saw", "tape", "bucket", "soap", "vacuum",
            "home", "flat", "place", "stay", "live", "rent", "own",
            "warm", "quiet", "safe", "repair", "balcony",
            # Food
            "bread", "meat", "cheese", "rice", "soup", "fish", "salt", "sugar",
            "milk", "egg", "cake", "pie", "fruit", "apple", "lemon",
            "bean", "corn", "nut", "oil", "honey", "sauce", "cream",
            "butter", "steak", "salad", "toast", "jam", "tea", "wine", "beer",
            "juice", "water", "meal", "dish", "cook", "taste", "bite", "feed",
            "eat", "drink", "slice", "chop", "boil", "fry", "bake", "grill",
            "roast", "stir", "mix", "pour", "serve", "plate", "bowl", "cup",
            "fork", "knife", "spoon", "pan", "pot", "oven", "stove",
            "fresh", "sweet", "sour", "bitter", "hot", "cold", "raw",
            "frozen", "spicy", "soft", "thick", "thin",
            "lunch", "dinner", "breakfast", "snack", "feast", "recipe",
            "pepper", "garlic", "ginger", "grain",
            "pasta", "pizza", "burger", "sandwich", "chicken", "pork", "beef",
            "lamb", "shrimp", "lobster", "bacon", "sausage", "ham",
            "candy", "chocolate", "cookie", "banana", "cherry", "peach",
        ],
        [
            # Дом
            "дом", "дверь", "окно", "стена", "пол", "крыша", "комната", "кровать",
            "стул", "стол", "лампа", "зеркало", "ванна", "лестница", "ключ",
            "замок", "забор", "сад", "двор", "диван", "полка", "ковер",
            "подушка", "шкаф", "гараж", "чердак",
            "кирпич", "стекло", "труба", "гвоздь", "краска", "пыль",
            "кухня", "балкон", "потолок", "порог", "крыльцо", "печь",
            "спальня", "подвал", "одеяло", "ящик",
            "душ", "батарея", "свет",
            "молоток", "пила", "ведро", "мыло",
            "квартира", "жилье", "уют", "тишина",
            "ремонт", "мебель", "камин", "веранда", "калитка", "ворота",
            "провод", "кран", "раковина",
            "плита", "холодильник", "полотенце", "покрывало",
            "табурет", "кресло", "комод", "люстра",
            "коридор", "паркет", "посуда", "чайник", "веник",
            # Еда
            "хлеб", "мясо", "сыр", "рис", "суп", "рыба", "соль", "сахар",
            "молоко", "яйцо", "торт", "пирог", "фрукт", "яблоко", "виноград", "лимон",
            "лук", "орех", "масло", "мед", "сливки",
            "каша", "салат", "чай", "вино", "пиво",
            "сок", "вода", "блюдо", "повар", "вкус", "кусок", "обед", "ужин",
            "завтрак", "перец", "капуста", "морковь", "картошка",
            "варить", "жарить", "резать",
            "тарелка", "чашка", "миска", "вилка", "нож", "ложка",
            "свежий", "сладкий", "горький", "острый",
            "рецепт", "чеснок", "зерно", "мука", "тесто",
            "курица", "колбаса", "конфета", "шоколад", "печенье",
            "борщ", "пельмени", "блины", "варенье", "компот",
            "сметана", "творог", "бульон",
            "помидор", "огурец", "свекла", "тыква", "грибы",
        ],
    ),
    (
        "People & Feelings",
        "Люди и чувства",
        [
            # Family & people
            "mother", "father", "sister", "brother", "son", "daughter", "wife",
            "husband", "baby", "child", "uncle", "aunt", "cousin", "nephew",
            "niece", "twin", "bride", "groom", "parent", "family", "home",
            "love", "care", "bond", "trust", "name", "birth", "age", "grow",
            "life", "kid", "boy", "girl", "man", "woman", "old", "young",
            "marry", "wedding", "divorce", "raise", "adopt", "teach", "learn",
            "play", "share", "help", "protect", "support", "comfort",
            "house", "dinner", "meal", "garden", "pet", "holiday", "birthday",
            "gift", "party", "celebrate", "tradition", "generation",
            "grandfather", "grandmother", "grandson",
            "relative", "friend", "neighbor", "couple", "partner", "lover",
            "promise", "respect", "honor", "duty", "sacrifice",
            "gentle", "kind", "warm", "close", "dear", "proud",
            "happy", "together", "belong", "remember", "forget",
            "youth", "adult", "senior", "guardian", "orphan",
            # Emotions
            "hate", "fear", "joy", "anger", "hope", "pride", "shame",
            "grief", "doubt", "envy", "guilt", "calm", "shock", "worry",
            "pain", "laugh", "smile", "cry", "sigh", "mood", "rage", "peace",
            "sad", "glad", "sorry", "brave", "shy", "hurt", "weak", "bold",
            "soft", "hard", "sweet", "bitter",
            "feel", "think", "wish", "want", "need", "like", "miss",
            "mind", "soul", "spirit", "heart", "dream", "thought", "memory",
            "passion", "desire", "pleasure", "relief", "wonder",
            "surprise", "terror", "horror", "panic", "stress", "tension",
            "anxiety", "delight", "sorrow", "regret", "pity",
            "mercy", "grace", "faith", "belief", "despair", "lonely",
            "cruel", "fierce", "tender", "nervous", "excited",
            "bored", "confused", "afraid", "angry", "upset", "pleased",
            "grateful", "jealous", "curious", "patient",
            "tired", "restless", "content", "humble", "selfish",
            "generous", "loyal", "honest", "sincere", "devoted",
        ],
        [
            # Семья и люди
            "мать", "отец", "сестра", "брат", "сын", "дочь", "жена",
            "муж", "ребенок", "дядя", "тетя", "племянник",
            "невеста", "жених", "семья", "дом",
            "любовь", "забота", "имя", "рождение", "возраст",
            "жизнь", "мальчик", "девочка", "мужчина", "женщина",
            "бабушка", "дедушка", "внук", "внучка", "родня", "свадьба",
            "наследник", "потомок", "поколение",
            "развод", "праздник", "подарок",
            "традиция", "предок", "родственник",
            "друг", "сосед", "пара", "партнер",
            "обещание", "уважение", "честь", "долг", "жертва",
            "добрый", "теплый", "близкий", "дорогой", "гордый",
            "счастливый", "молодой", "старый", "взрослый",
            "младенец", "малыш", "подросток", "юноша", "девушка",
            "сирота", "отчим",
            "няня", "наставник",
            "зять", "свекровь", "теща", "тесть",
            "родители", "дети", "супруг",
            # Эмоции
            "страх", "радость", "гнев", "надежда", "гордость", "стыд",
            "горе", "зависть", "вина", "покой", "боль",
            "смех", "улыбка", "крик", "вздох", "ярость", "счастье",
            "грусть", "нежность", "тоска", "обида", "ужас", "злость",
            "печаль", "восторг", "тревога", "скука", "жалость", "досада",
            "отчаяние", "смелость", "сочувствие",
            "чувство", "мысль", "желание", "мечта", "память", "душа", "дух",
            "страсть", "удовольствие", "утешение", "облегчение",
            "удивление", "паника", "стресс", "напряжение",
            "наслаждение", "сожаление", "милость", "вера",
            "жестокий", "нервный",
            "скучный", "испуганный", "сердитый",
            "терпеливый", "усталый", "довольный", "щедрый", "верный", "честный",
            "ласковый", "грубый", "злой",
            "веселый", "грустный", "спокойный", "тревожный", "мрачный",
            "сострадание", "благодарность",
            "волнение", "беспокойство", "разочарование",
            "злоба", "ненависть", "презрение",
            "восхищение", "изумление", "замешательство",
        ],
    ),
    (
        "City & Work",
        "Город и работа",
        [
            # City
            "street", "road", "bridge", "tower", "store", "shop", "park",
            "church", "school", "bank", "hotel", "market", "square", "train",
            "bus", "car", "taxi", "crowd", "noise", "sign", "light", "block",
            "corner", "lane", "gate", "bench", "clock", "wall",
            "roof", "floor", "step", "path", "walk", "ride", "stop", "turn",
            "city", "town", "village", "district", "zone", "area", "center",
            "station", "airport", "port", "harbor", "dock", "pier",
            "highway", "alley", "avenue",
            "traffic", "parking", "building", "office", "factory",
            "warehouse", "stadium", "theater", "museum", "library",
            "hospital", "prison", "police", "ambulance",
            "restaurant", "bar", "cafe", "cinema", "gallery",
            "fountain", "statue", "palace",
            "electric", "gas", "subway", "ferry",
            "citizen", "tourist", "visitor", "resident",
            "mayor", "council", "downtown",
            # Work
            "work", "boss", "team", "task", "goal", "plan", "deal", "trade",
            "job", "pay", "hire", "fire", "lead", "build", "sell", "buy",
            "earn", "spend", "save", "risk", "gain", "loss", "cost", "price",
            "debt", "loan", "tax", "fund", "stock", "firm", "staff",
            "skill", "tool", "file", "desk", "note", "rule", "law",
            "meeting", "project", "deadline", "budget", "report",
            "contract", "salary", "bonus", "profit", "expense",
            "client", "customer", "partner", "manager",
            "director", "president", "secretary",
            "engineer", "lawyer", "doctor", "teacher", "writer",
            "artist", "designer",
            "interview", "resume", "career", "promotion", "transfer",
            "retire", "pension", "vacation", "overtime", "shift",
            "workshop", "laboratory",
            "success", "failure", "progress", "growth",
            "compete", "negotiate", "propose", "approve", "reject",
            "schedule", "organize", "manage",
        ],
        [
            # Город
            "улица", "дорога", "мост", "башня", "магазин", "парк",
            "церковь", "школа", "банк", "отель", "рынок", "площадь", "поезд",
            "автобус", "машина", "такси", "толпа", "шум", "знак", "свет",
            "угол", "переход", "ворота", "часы", "стена",
            "крыша", "тротуар", "перекресток", "фонарь", "вокзал",
            "метро", "кафе", "ресторан", "театр", "музей",
            "город", "поселок", "деревня", "район", "центр",
            "станция", "аэропорт", "порт", "причал",
            "шоссе", "переулок", "проспект", "бульвар",
            "здание", "офис", "завод",
            "склад", "стадион", "библиотека",
            "больница", "тюрьма", "полиция", "пожарный",
            "бар", "галерея",
            "фонтан", "памятник", "собор", "дворец",
            "трамвай", "паром",
            "житель", "турист", "гость", "мэр",
            "пригород", "набережная", "сквер",
            "остановка", "аллея", "арка", "колонна",
            "этаж", "подъезд", "двор", "квартал",
            "почта", "аптека",
            # Работа
            "работа", "начальник", "команда", "задача", "цель", "план",
            "должность", "зарплата", "успех", "провал",
            "доход", "расход", "риск", "прибыль", "цена",
            "долг", "кредит", "налог", "бюджет", "фирма", "штат",
            "проект", "отчет", "договор", "офис", "карьера",
            "опыт", "клиент", "партнер", "контракт", "премия",
            "совещание", "встреча", "срок", "график",
            "директор", "секретарь",
            "инженер", "юрист", "врач", "учитель", "писатель",
            "художник",
            "резюме", "повышение", "перевод",
            "пенсия", "отпуск", "смена",
            "мастерская", "лаборатория",
            "прогресс", "рост",
            "коллега", "руководитель", "заместитель",
            "специалист", "предприниматель",
            "производство", "товар", "услуга",
            "капитал", "увольнение", "набор",
        ],
    ),
    (
        "Body & Health",
        "Тело и здоровье",
        [
            "head", "hand", "heart", "eye", "ear", "nose", "mouth", "arm",
            "leg", "foot", "bone", "skin", "blood", "brain", "face", "neck",
            "chest", "back", "knee", "finger", "tooth", "hair", "lip", "nail",
            "lung", "muscle", "palm", "thumb", "jaw", "hip",
            "wrist", "skull", "spine", "gut", "fist", "heel",
            "body", "breath", "pulse", "nerve", "pain", "sick",
            "health", "strong", "weak", "fit", "tired", "sleep", "wake",
            "walk", "run", "stand", "sit", "lie", "bend", "stretch",
            "touch", "feel", "see", "hear", "smell", "taste",
            "eat", "drink", "swallow", "chew", "cough",
            "bleed", "heal", "hurt", "burn", "cut", "scar",
            "wound", "fever", "cold", "flu", "doctor", "nurse", "cure",
            "medicine", "pill", "drug", "surgery", "hospital",
            "diet", "exercise", "weight", "height", "age",
            "shoulder", "ankle", "belly",
            "tongue", "cheek", "chin", "forehead",
            "joint", "organ", "tissue",
            "stomach", "liver", "kidney", "vessel",
        ],
        [
            "голова", "рука", "сердце", "глаз", "ухо", "нос", "рот", "нога",
            "кость", "кожа", "кровь", "мозг", "лицо", "шея",
            "грудь", "спина", "колено", "палец", "зуб", "волос", "губа", "ноготь",
            "ладонь", "череп", "кулак", "пятка",
            "плечо", "живот", "бровь", "лоб", "борода", "щека", "локоть",
            "ребро", "горло", "язык",
            "тело", "дыхание", "пульс", "боль", "здоровье",
            "сильный", "слабый", "усталый", "сон", "ходить", "бежать",
            "стоять", "сидеть", "лежать",
            "трогать", "чувствовать", "видеть", "слышать",
            "есть", "пить", "глотать", "жевать", "кашель",
            "лечить", "ранить", "шрам",
            "рана", "температура", "простуда", "доктор", "врач", "лекарство",
            "таблетка", "больница", "операция",
            "диета", "вес", "рост", "возраст",
            "бедро", "подбородок", "затылок",
            "сустав", "орган", "ткань",
            "желудок", "печень", "легкое",
            "позвоночник", "запястье",
            "ступня", "мизинец",
            "зрачок", "челюсть",
            "мышца", "нерв",
            "скула", "висок", "лопатка",
            "пищевод", "селезенка",
        ],
    ),
    (
        "War & Time",
        "Война и время",
        [
            # War
            "war", "peace", "army", "fight", "battle", "sword", "shield",
            "gun", "bomb", "tank", "ship", "plane", "camp", "fort", "flag",
            "march", "charge", "attack", "defend", "guard", "spy", "trap",
            "raid", "fire", "shot", "wound", "blood", "death",
            "hero", "soldier", "enemy", "ally", "chief", "rank", "order",
            "victory", "defeat", "weapon", "armor", "bullet", "missile",
            "rifle", "cannon", "mine", "explosive",
            "general", "colonel", "captain", "sergeant", "private",
            "navy", "marine", "pilot",
            "bunker", "fortress", "castle", "wall",
            "scout", "sniper", "engineer", "commander",
            "mission", "operation", "campaign",
            "retreat", "surrender", "capture", "escape", "rescue",
            "patrol", "supply",
            "destroy", "conquer",
            "treaty", "alliance",
            "revolution", "civil", "conflict", "crisis",
            "courage", "honor", "duty", "sacrifice", "glory",
            # Time
            "time", "hour", "minute", "second", "day", "night", "week",
            "month", "year", "past", "future", "now", "then", "soon",
            "late", "early", "fast", "slow", "rush", "wait", "start",
            "end", "begin", "finish", "dawn", "noon", "clock",
            "watch", "date", "season", "spring", "summer", "winter",
            "fall", "morning", "evening", "afternoon", "midnight",
            "today", "tomorrow", "yesterday", "always", "never",
            "often", "sometimes", "rarely", "once", "twice",
            "forever", "moment", "instant", "period", "era",
            "century", "decade", "lifetime", "generation", "history",
            "ancient", "modern", "recent", "current", "previous",
            "next", "last", "first", "final",
            "schedule", "deadline", "appointment", "calendar",
            "alarm", "delay", "hurry", "patience",
            "eternal", "temporary", "permanent", "brief", "long",
            "young", "old", "new",
            "birthday", "anniversary", "holiday", "festival",
            "sunrise", "sunset", "twilight",
            "routine", "habit", "rhythm", "cycle", "phase",
        ],
        [
            # Война
            "война", "мир", "армия", "битва", "меч", "щит",
            "пушка", "бомба", "танк", "корабль", "лагерь", "крепость", "флаг",
            "марш", "атака", "оборона", "стража", "ловушка",
            "огонь", "выстрел", "рана", "кровь", "смерть",
            "герой", "солдат", "враг", "приказ",
            "победа", "поражение", "оружие", "пуля", "сражение",
            "генерал", "полковник", "капитан", "сержант", "рядовой",
            "пехота", "флот", "пилот",
            "окоп", "стена",
            "разведчик", "снайпер", "командир",
            "миссия", "операция", "кампания",
            "отступление", "плен", "побег", "спасение",
            "патруль", "конвой",
            "оккупация", "освобождение",
            "договор", "союз", "восстание",
            "революция", "конфликт", "кризис",
            "мужество", "честь", "долг", "жертва", "слава",
            "штурм", "блокада", "десант", "артиллерия",
            "гарнизон", "штаб", "караул",
            "знамя", "орден", "снаряд", "взрыв", "обстрел",
            # Время
            "время", "час", "минута", "секунда", "день", "ночь", "неделя",
            "месяц", "год", "возраст", "прошлое", "будущее", "сейчас",
            "рассвет", "закат", "полдень", "часы",
            "дата", "сезон", "весна", "лето", "зима", "осень",
            "срок", "период", "эпоха", "мгновение", "вечность",
            "утро", "вечер", "полночь", "столетие",
            "календарь", "расписание",
            "терпение", "спешка",
            "молодой", "старый", "новый", "свежий",
            "праздник", "юбилей",
            "вечный", "временный", "постоянный", "краткий", "долгий",
            "сегодня", "завтра", "вчера", "всегда", "никогда",
            "часто", "иногда", "редко", "однажды", "дважды",
            "навсегда", "момент", "миг", "пора",
            "древний", "современный", "недавний", "нынешний", "прежний",
            "следующий", "последний", "первый",
            "привычка", "ритм", "цикл",
            "сумерки", "заря",
            "поколение", "история",
        ],
    ),
]


def main():
    en_dict = load_dictionary("en")
    ru_dict = load_dictionary("ru")

    en_themes = []
    ru_themes = []
    removed = []

    print(f"English dictionary: {len(en_dict)} words")
    print(f"Russian dictionary: {len(ru_dict)} words")
    print(f"Minimum words per theme: {MIN_WORDS_PER_THEME}")
    print()

    for en_name, ru_name, en_words, ru_words in THEMES:
        valid_en = validate_and_filter(en_words, en_dict)
        valid_ru = validate_and_filter(ru_words, ru_dict)

        missing_en = set(w.lower() for w in en_words if len(w) >= 3) - set(valid_en)
        missing_ru = set(w.lower() for w in ru_words if len(w) >= 3) - set(valid_ru)

        en_freq = sum(en_dict[w] for w in valid_en)
        ru_freq = sum(ru_dict[w] for w in valid_ru)

        keep = len(valid_en) >= MIN_WORDS_PER_THEME and len(valid_ru) >= MIN_WORDS_PER_THEME
        status = "KEEP" if keep else "REMOVED"

        print(f"[{en_name} / {ru_name}] — {status}")
        print(f"  EN: {len(valid_en)} words, total freq={en_freq:,}")
        if missing_en:
            print(f"  EN missing ({len(missing_en)}): {sorted(missing_en)[:10]}{'...' if len(missing_en) > 10 else ''}")
        print(f"  RU: {len(valid_ru)} words, total freq={ru_freq:,}")
        if missing_ru:
            print(f"  RU missing ({len(missing_ru)}): {sorted(missing_ru)[:10]}{'...' if len(missing_ru) > 10 else ''}")
        print()

        if keep:
            en_themes.append({"name": en_name, "words": sorted(valid_en)})
            ru_themes.append({"name": ru_name, "words": sorted(valid_ru)})
        else:
            removed.append(f"{en_name}/{ru_name} (EN={len(valid_en)}, RU={len(valid_ru)})")

    print("=" * 60)
    print(f"Kept: {len(en_themes)} themes")
    if removed:
        print(f"Removed: {', '.join(removed)}")
    print()

    print(f"{'Theme':<25} {'EN words':>10} {'EN freq':>12} {'RU words':>10} {'RU freq':>12}")
    print("-" * 71)
    for i in range(len(en_themes)):
        en_f = sum(en_dict[w] for w in en_themes[i]["words"])
        ru_f = sum(ru_dict[w] for w in ru_themes[i]["words"])
        print(f"{en_themes[i]['name']:<25} {len(en_themes[i]['words']):>10} {en_f:>12,} {len(ru_themes[i]['words']):>10} {ru_f:>12,}")

    en_path = ASSETS / "themes.en.json"
    ru_path = ASSETS / "themes.ru.json"

    with open(en_path, "w", encoding="utf-8") as f:
        json.dump({"themes": en_themes}, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {en_path}")

    with open(ru_path, "w", encoding="utf-8") as f:
        json.dump({"themes": ru_themes}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {ru_path}")


if __name__ == "__main__":
    main()
