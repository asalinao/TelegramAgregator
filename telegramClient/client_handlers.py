import os
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from telethon import utils
from telethon.tl.types import MessageMediaDocument, DocumentAttributeSticker

from database.db import get_subscribed_users, get_channel_link_by_id, add_keywords, add_ticker
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
    if not users:
        return

    if text:
        tickers, keywords = get_all_hotwords(text)

        keywords_string = " ".join(keywords)
        add_keywords(chat_id, text, keywords_string)

        for ticker in tickers:
            add_ticker(chat_id, ticker)


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
                reply_markup=link_button('Link to error message', link)
            )

    for media in media_list:
        os.remove(media)



async def handler_single(event):
    message = event.message

    if isinstance(message.media, MessageMediaDocument):
        for attr in message.media.document.attributes:
            if isinstance(attr, DocumentAttributeSticker):
                return

    chat = event.chat.title
    chat_id = int(utils.resolve_id(event.chat_id)[0])
    message_id = event.id
    text = event.text

    link = get_message_link(chat_id, message_id)
    users = get_subscribed_users(chat_id)
    if not users:
        return

    if text:
        tickers, keywords = get_all_hotwords(text)

        keywords_string = " ".join(keywords)
        add_keywords(chat_id, text, keywords_string)

        for ticker in tickers:
            add_ticker(chat_id, ticker)

    if message.photo:
        photo = await event.download_media()
        for user_id in users:
            try:
                await bot.send_photo(user_id, photo=FSInputFile(photo), caption=text, reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button('Link to error message', link))
        os.remove(photo)
    elif message.document:
        document = await event.download_media()
        for user_id in users:
            try:
                await bot.send_document(user_id, document=FSInputFile(document), caption=text,
                                        reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button('Link to error message', link))
        os.remove(document)
    else:
        for user_id in users:
            try:
                await bot.send_message(user_id, text, reply_markup=link_button(chat, link), parse_mode='Markdown')
            except Exception as ex:
                await bot.send_message(user_id, ex.message , reply_markup=link_button('Link to error message', link))
