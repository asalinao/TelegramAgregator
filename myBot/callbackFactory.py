from aiogram.filters.callback_data import CallbackData


class ButtonsCallbackFactory(CallbackData, prefix="buttfab"):
    id: int
    link: str
