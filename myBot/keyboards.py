from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from myBot.callbackFactory import ButtonsCallbackFactory

show_my_channel_list = KeyboardButton(text='Show my channel list')
show_wordcloud_24 = KeyboardButton(text='Show 24h wordcloud')

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[show_my_channel_list], [show_wordcloud_24]],
    resize_keyboard=True
)


empty_channel_list_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Add channel', callback_data='add_channel')],
                     [InlineKeyboardButton(text='I want to go back', callback_data='go_back')]]
)


def link_button(name, link):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=name,
        url=link
    )
    builder.button(
        text="translate_text",
        callback_data='translate_text'
    )
    builder.adjust(1)
    return builder.as_markup()


def second_link_button(button):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=button.text,
        url=button.url
    )
    builder.button(
        text="Translate text",
        callback_data='translate_text'
    )
    builder.adjust(1)
    return builder.as_markup()


def translate_back(button):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=button.text,
        url=button.url
    )
    builder.button(
        text="View original",
        callback_data='view_original'
    )
    builder.adjust(1)
    return builder.as_markup()


def channel_remove_keyboard(channels_dict):
    builder = InlineKeyboardBuilder()
    for key, value in channels_dict.items():
        builder.button(
            text=f"{value[0]} ({key})",
            callback_data=ButtonsCallbackFactory(id=key, name=value[0], link=value[1].split('/')[-1])
        )

    builder.adjust(1)
    return builder.as_markup()


def channel_list_keyboard(channels_dict):
    buttons = []
    for key, value in channels_dict.items():
        button = InlineKeyboardButton(
            text=f"{value[0]} ({key})",
            url=value[1]
        )

        buttons.append([button])

    add_channel = InlineKeyboardButton(text='Add channel', callback_data='add_channel')
    remove_channel = InlineKeyboardButton(text='Remove channel', callback_data='remove_channel')
    i_want_to_go_back = InlineKeyboardButton(text='I want to go back', callback_data='go_back')

    buttons.append([add_channel, remove_channel])
    buttons.append([i_want_to_go_back])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
