import asyncio
import logging
import os
import dotenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import router

logger = logging.getLogger(__name__)

dotenv.load_dotenv('.env')


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot...')
    bot = Bot(os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    logger.info('Including routers...')
    dp.include_router(router)
    dp['repost_chat_id'] = int(os.getenv('CHAT_ID'))

    logger.info('Running polling...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
