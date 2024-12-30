import os
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from telethon import utils

from database.db import get_subscribed_users, get_channel_link_by_id, add_message
from config import BOT_TOKEN
from myBot.keyboards import link_button
from services.keywords import get_all_hotwords


def get_message_link(chat_id, message_id):
    chat_link = get_channel_link_by_id(chat_id)
    if chat_link is None:
        return
    if '+' in chat_link:
        return f"t.me/c/{chat_id}/{message_id}"
    else:
        return f"{chat_link}/{message_id}"
    
    
bot = Bot(token=BOT_TOKEN)  

async def handler_album(event):
    chat_id = int(utils.resolve_id(event.chat_id)[0])
    message_id = event[0].id
    chat = event.chat.title
    text = event.text

    link = get_message_link(chat_id, message_id)
    users = get_subscribed_users(chat_id)

    if text:
        keywords_string = " ".join(get_all_hotwords(text))
        add_message(chat_id, keywords_string)

    media_group = MediaGroupBuilder()
    media_list = []

    for media in event.__iter__():
        file = await media.download_media()
        media_list.append(file)
        if media.photo:
            media_group.add_photo(media=FSInputFile(file))
        elif media.video:
            media_group.add_video(media=FSInputFile(file))
        elif media.document:
            media_group.add_document(media=FSInputFile(file))
        elif media.audio:
            media_group.add_audio(media=FSInputFile(file))

    for user_id in users:
        try:
            await bot.send_media_group(chat_id=user_id, media=media_group.build())
            await bot.send_message(
                user_id,
                text,
                reply_markup=link_button(chat, link),
                parse_mode='Markdown'
            )
        except Exception as ex:
             await bot.send_message(
                user_id,
                ex.message,
                reply_markup=link_button(chat, link)
            )

    for media in media_list:
        os.remove(media)



async def handler_single(event):
    message = event.message
    chat = event.chat.title
    chat_id = int(utils.resolve_id(event.chat_id)[0])
    message_id = event.id
    text = event.text

    link = get_message_link(chat_id, message_id)
    users = get_subscribed_users(chat_id)

    if text:
        keywords_string = " ".join(get_all_hotwords(text))
        add_message(chat_id, keywords_string)

    if message.photo:
        photo = await event.download_media()
        for user_id in users:
            try:
                await bot.send_photo(user_id, photo=FSInputFile(photo), caption=text, reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button(chat, link))
        os.remove(photo)
    elif message.document:
        document = await event.download_media()
        for user_id in users:
            try:
                await bot.send_document(user_id, document=FSInputFile(document), caption=text,
                                        reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button(chat, link))
        os.remove(document)
    else:
        for user_id in users:
            try:
                await bot.send_message(user_id, text, reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button(chat, link))
