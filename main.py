import asyncio

from telegramClient.client_methods import start_parsing
from myBot.bot_start import start_bot
from database.db import create_database


async def main():
    await asyncio.gather(start_bot(), start_parsing())


if __name__ == "__main__":
    create_database()
    asyncio.run(main())
