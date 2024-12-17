from aiogram import Bot, Dispatcher

from myBot.bot_handlers import router
from config import BOT_TOKEN


async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())