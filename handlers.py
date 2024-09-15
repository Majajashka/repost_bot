import logging

from aiogram import Router, Bot
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import Message, ChatMemberUpdated

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


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
    ChatTypeFilter('channel')
)
async def added_groups(event: ChatMemberUpdated, bot: Bot, admin_id: int):
    if event.from_user.id == admin_id:
        logging.info(
            "Bot has been successfully added to the channel '%s' with id %s by the admin with id %s.",
            event.chat.title or "Unknown",
            event.chat.id,
            admin_id
        )
        await bot.send_message(chat_id=admin_id,
                               text=f"🎉 Бот был успешно добавлен в ваш канал: \n\n"

                                    f"Канал: {f'@{event.chat.username}' or f'<b>event.chat.title</b>' or '<b>Неизвестно</b>'}\n"
                                    f"ID: <code>{event.chat.id}</code>"
                               )
    else:
        logging.info(
            "Unauthorized attempt: User '%s' with id %s tried to add bot to channel '%s' with id %s. Lefting channel...",
            event.from_user.username or "Unknown",
            event.from_user.id,
            event.chat.title or "Unknown",
            event.chat.id
        )
        await event.chat.leave()
        logging.info(
            "Bot has successfully left the channel '%s' with id %s.",
            event.chat.title or "Unknown",
            event.chat.id
        )
        return
