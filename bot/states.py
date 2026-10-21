from aiomax2.fsm import StatesGroup, State


class ShelfStates(StatesGroup):
    waiting_for_data = State()    # ждём фото или Excel
    waiting_for_retake = State()  # ждём пересъёмку после плохого качества
