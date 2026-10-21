# TODO: заменить на yookassa / yookassax + вебхук подтверждения. ЗАГЛУШКА!
async def create_payment(user_id: str, amount: float = 990.0) -> dict:
    return {
        "payment_id": f"stub_{user_id}",
        "confirmation_url": "https://yookassa.ru/checkout/stub",
        "status": "pending",
    }
