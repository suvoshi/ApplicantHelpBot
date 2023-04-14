import aiogram as ai
import asyncio
from bot import config

config.load_env()

bot = ai.Bot(config.settings["token_api"])
dp = ai.Dispatcher(bot)


async def main():
    from bot.handlers import dp

    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
