import logging

from aiomax2 import Router, F
from aiomax2.filters import Command
from aiomax2.types import Message
from aiomax2.fsm import FSMManager, MemoryStorage
from aiomax2.utils.keyboard import InlineKeyboardBuilder

from .states import ShelfStates
from core.ocr import recognize_photo
from core.payments import create_payment
from core.excel_parser import parse_expiry_excel

logger = logging.getLogger(__name__)
router = Router()
fsm = FSMManager(MemoryStorage())


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 *Свежая полка*\n\n"
        "Пришлите *фото* таблицы приходов или *Excel-файл* — "
        "я найду товары с истекающим сроком.\n\n"
        "/photo — загрузить фото\n"
        "/file — загрузить Excel\n"
        "/pay — оплатить подписку\n"
        "/help — помощь",
        format="markdown",
    )
    await fsm.set_state(message.sender_id, str(ShelfStates.waiting_for_data), message.chat_id)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "1. Сфотографируйте таблицу при хорошем свете.\n"
        "2. Убедитесь, что вся таблица в кадре.\n"
        "3. Отправьте фото боту.\n"
        "4. Получите список товаров, которые скоро истекут.\n\n"
        "Если фото не распозналось — бот попросит переснять."
    )


@router.message(Command("pay"))
async def cmd_pay(message: Message):
    payment = await create_payment(str(message.sender_id))
    kb = InlineKeyboardBuilder()
    kb.button(text="💳 Перейти к оплате", url=payment["confirmation_url"])
    kb.adjust(1)
    await message.answer(
        "Подписка «Свежая полка» — 990 ₽/мес.\nНажмите кнопку для оплаты (заглушка).",
        reply_markup=kb.as_markup(),
    )


@router.message(F.photo)
async def handle_photo(message: Message):
    logger.info("Фото от %s", message.sender_id)
    file_bytes = await message.download_photo()
    await message.answer("🔍 Распознаю таблицу...")

    result = await recognize_photo(file_bytes)

    if not result["ok"]:
        await fsm.set_state(message.sender_id, str(ShelfStates.waiting_for_retake), message.chat_id)
        await message.answer(
            f"❌ Не удалось распознать таблицу.\n\n{result['reason']}\n\n"
            "Отправьте новое фото.",
            format="markdown",
        )
        return

    await _send_items(message, result["items"])
    await fsm.set_state(message.sender_id, str(ShelfStates.waiting_for_data), message.chat_id)


@router.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    if not doc.file_name.lower().endswith((".xlsx", ".xls")):
        await message.answer("Пришлите Excel-файл (.xlsx/.xls) или фото таблицы.")
        return

    await message.answer("📊 Обрабатываю Excel...")
    file_bytes = await message.download_document()

    # Сохраняем во временный файл — ваш парсер принимает путь
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        items = parse_expiry_excel(tmp_path)
    finally:
        os.unlink(tmp_path)

    await _send_items(message, items)


async def _send_items(message: Message, items: list):
    if not items:
        await message.answer("Товаров с истекающим сроком не найдено. 👍")
        return

    lines = ["⚠️ *Товары с истекающим сроком:*\n"]
    for item in items[:15]:
        lines.append(f"• {item['name']} — через {item['days_left']} дн. (до {item['expiry_date']})")
    if len(items) > 15:
        lines.append(f"\n... и ещё {len(items) - 15} позиций.")
    lines.append("\n💡 Распродайте или спишите.")
    await message.answer("\n".join(lines), format="markdown")
