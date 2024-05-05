from aiogram.fsm.state import StatesGroup, State


class FSM(StatesGroup):
    add_channel = State()
