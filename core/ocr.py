 # TODO: заменить на Tesseract / Yandex Vision + препроцессинг (поворот, контраст). ЗАГЛУШКА!
_call_counter = 0


async def recognize_photo(file_bytes: bytes) -> dict:
    global _call_counter
    _call_counter += 1

    if _call_counter % 3 == 0:
        return {
            "ok": False,
            "reason": (
                "Фото размытое или тёмное. Попробуйте:\n"
                "• включить свет\n"
                "• положить таблицу ровно\n"
                "• не трясти телефон во время съёмки\n"
                "• убедиться, что вся таблица в кадре"
            ),
        }

    return {
        "ok": True,
        "items": [
            {"name": "Молоко (пример)", "expiry_date": "2025-11-01", "days_left": 7},
            {"name": "Йогурт (пример)", "expiry_date": "2025-10-28", "days_left": 3},
        ],
    }
