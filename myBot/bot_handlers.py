from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
import os

from myBot.callbackFactory import ButtonsCallbackFactory
from myBot.keyboards import main_keyboard, channel_list_keyboard, empty_channel_list_keyboard, channel_remove_keyboard, \
    translate_back, second_link_button
from services.translator import translate_text
from telegramClient.client_methods import join_channel, leave_from_channel
from myBot.states import FSM
from database.db import add_user, add_channel_and_subscription, remove_subscription, get_user_subscribed_channels, \
    check_channel_exists, get_text, delete_text, add_text, get_keywords_by_user_id
from services.wordcloud import cloud_generate



router = Router()


@router.message(Command("start"), StateFilter(default_state))
async def start_handler(message: Message):
    add_user(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
    await message.answer(
        "It`s aggregator bot!",
        reply_markup=main_keyboard
    )


@router.message(F.text == 'Show my channel list', StateFilter(default_state))
async def show_channel_list(message: Message):
    channel_dict = get_user_subscribed_channels(message.chat.id)
    if len(channel_dict) == 0:
        await message.answer(
            text='Your list is empty.',
            reply_markup=empty_channel_list_keyboard
        )
    else:
        await message.answer(
            text=f"This is your channel list:",
            reply_markup=channel_list_keyboard(channel_dict)
        )


@router.message(F.text == 'Show 24h wordcloud', StateFilter(default_state))
async def show_wordcloud_24(message: Message):
    keywords = get_keywords_by_user_id(message.chat.id)

    if len(keywords) == 0:
        await message.answer('We need at least 1 word to plot a word cloud, got 0.')

    else:
        filename = f'plot{str(message.chat.id)}.png'

        cloud_generate(keywords, filename)

        photo = FSInputFile(filename)
        await message.answer_photo(photo=photo)
        os.remove(filename)

    

@router.callback_query(F.data == 'add_channel', StateFilter(default_state))
async def add_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    await callback.message.edit_text(text='Send me new channel link, please')
    await state.set_state(FSM.add_channel)


@router.message(StateFilter(FSM.add_channel))
async def channel_to_add_sent(message: Message, state: FSMContext):
    result = await join_channel(message.text)

    if type(result) == list:
        add_channel_and_subscription(message.chat.id, result[0], message.text, result[1])
        await message.answer('Success!')
    else:
        await message.answer(f'Error: {result}')

    await show_channel_list(message)
    await state.clear()


@router.callback_query(F.data == 'remove_channel', StateFilter(default_state))
async def remove_channel(callback: CallbackQuery):
    channel_dict = get_user_subscribed_channels(callback.message.chat.id)
    await callback.message.edit_text("Select the channel to remove:")
    await callback.message.edit_reply_markup(
        reply_markup=channel_remove_keyboard(channel_dict)
    )


@router.callback_query(ButtonsCallbackFactory.filter())
async def callbacks_num_change_fab(callback: CallbackQuery, callback_data: ButtonsCallbackFactory):
    channel_id = callback_data.id
    channel_link = f"https://t.me/{callback_data.link}"

    remove_subscription(callback.from_user.id, channel_id)
    if not check_channel_exists(channel_id):
        await leave_from_channel(channel_link)

    channel_dict = get_user_subscribed_channels(callback.message.chat.id)
    if len(channel_dict) == 0:
        await callback.message.edit_text(
            text='Your list is empty.'
        )
        await callback.message.edit_reply_markup(
            reply_markup=empty_channel_list_keyboard
        )
    else:
        await callback.message.edit_text(
            text=f"This is your channel list:",
        )
        await callback.message.edit_reply_markup(
            reply_markup=channel_list_keyboard(channel_dict)
        )


@router.callback_query(F.data == 'go_back', StateFilter(default_state))
async def go_back(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    await callback.message.answer('You are now in the main menu!', reply_markup=main_keyboard)


@router.callback_query(F.data == 'translate_text', StateFilter(default_state))
async def translate_text_callback(callback: CallbackQuery):
    if callback.message.caption:
        text_to_translate = callback.message.caption
    else:
        text_to_translate = callback.message.text

    translated_text = translate_text(text_to_translate)

    button = callback.message.reply_markup.inline_keyboard[0][0]

    if callback.message.caption:
        await callback.message.edit_caption(caption=translated_text, reply_markup=translate_back(button))
        add_text(message_id=callback.message.message_id, text=callback.message.caption)
    else:
        await callback.message.edit_text(text=translated_text, reply_markup=translate_back(button))
        add_text(message_id=callback.message.message_id, text=callback.message.text)


@router.callback_query(F.data == 'view_original', StateFilter(default_state))
async def view_original_callback(callback: CallbackQuery):
    original_text = get_text(callback.message.message_id)
    button = callback.message.reply_markup.inline_keyboard[0][0]

    if callback.message.caption:
        await callback.message.edit_caption(caption=original_text, parse_mode="Markdown", reply_markup=second_link_button(button))
    else:
        await callback.message.edit_text(text=original_text, parse_mode="Markdown", reply_markup=second_link_button(button))
    delete_text(callback.message.message_id)

