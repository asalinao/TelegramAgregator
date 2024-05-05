import asyncio

from telegramClient.client_methods import start_parsing
from myBot.bot_start import start_bot


async def main():
    await asyncio.gather(start_bot(), start_parsing())


if __name__ == "__main__":
    asyncio.run(main())


