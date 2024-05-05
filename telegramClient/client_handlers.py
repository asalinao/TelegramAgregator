import shutil
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from telethon import utils
import os

from database.db import get_subscribed_users, get_channel_link_by_id
from config import BOT_TOKEN
from myBot.keyboards import link_button


def get_message_link(chat_id, message_id):
    chat_link = get_channel_link_by_id(chat_id)
    if '+' in chat_link:
        return f"t.me/c/{chat_id}/{message_id}"
    else:
        return f"{chat_link}/{message_id}"


async def handlerAlbum(event):
    bot = Bot(token=BOT_TOKEN)

    chat_id = int(utils.resolve_id(event.chat_id)[0])
    message_id = event.id

    link = get_message_link(chat_id, message_id)

    users = get_subscribed_users(chat_id)

    text = event.text

    for user_id in users:
        media_group = MediaGroupBuilder(caption=f'{text}\n\nAuthor`s channel link: t.me/{link.split("/")[-1]}')

        for media in event.__iter__():
            file = await media.download_media('./bufferdata/')
            if media.photo:
                media_group.add_photo(media=FSInputFile(file))
            elif media.video:
                media_group.add_video(media=FSInputFile(file))
            elif media.document:
                media_group.add_document(media=FSInputFile(file))
            elif media.audio:
                media_group.add_audio(media=FSInputFile(file))

        await bot.send_media_group(chat_id=user_id, media=media_group.build())

        shutil.rmtree('./bufferdata/')


async def handlerSingle(event):
    bot = Bot(token=BOT_TOKEN)

    message = event.message

    chat = event.chat.title

    chat_id = int(utils.resolve_id(event.chat_id)[0])
    message_id = event.id

    link = get_message_link(chat_id, message_id)

    users = get_subscribed_users(chat_id)

    text = event.text

    for user_id in users:
        if message.photo:
            photo = await event.download_media('./bufferdata/')
            await bot.send_photo(user_id, photo=FSInputFile(photo), caption=text, reply_markup=link_button(chat, link), parse_mode='Markdown')
            shutil.rmtree('./bufferdata/')

        elif message.document:
            document = await event.download_media('./bufferdata/')
            await bot.send_document(user_id, document=FSInputFile(document), caption=text,
                                    reply_markup=link_button(chat, link), parse_mode='Markdown')
            shutil.rmtree('./bufferdata/')

        else:
            await bot.send_message(user_id, text, reply_markup=link_button(chat, link), parse_mode='Markdown')
