import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import ChatTypeFilter

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.channel_post(ChatTypeFilter('channel'))
async def repost_channel_message(message: Message, repost_chat_id: int):
    logger.info('Message from channel %s forwarded to chat %s', message.chat.id, repost_chat_id)
    await message.copy_to(repost_chat_id)


@router.message(Command('get_chat_id'))
async def get_chat_id(message: Message):
    await message.answer(
        'Chat id:\n'
        f'<code>{message.chat.id}</code>'
    )
