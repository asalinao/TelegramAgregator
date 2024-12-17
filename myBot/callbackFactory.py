from aiogram.filters.callback_data import CallbackData


class ButtonsCallbackFactory(CallbackData, prefix="buttfab"):
    id: int
    name: str
    link: str
