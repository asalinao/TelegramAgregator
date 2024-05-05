from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from config import API_ID, API_HASH
from telegramClient.client_handlers import handler_single, handler_album


client = TelegramClient('test_tg', API_ID, API_HASH, device_model="iPhone 55 Pro", system_version="IOS 100.1")


async def start_parsing():
    client.add_event_handler(handler_album, events.Album())
    client.add_event_handler(handler_single, events.NewMessage(func=lambda e: e.grouped_id is None))
    await client.start()
    await client.run_until_disconnected()


async def join_channel(link):
    await client.start()
    try:
        entity = await client.get_entity(link)
    except ValueError:
        try:
            updates = await client(ImportChatInviteRequest(link.split('+')[1]))
            return [updates.chats[0].id, updates.chats[0].title]
        except Exception as e:
            if 'A wait of' in str(e):
                return 'Try again later.'

    try:
        await client(JoinChannelRequest(entity))
        return [entity.id, entity.title]
    except:
        return "Not found"


async def leave_from_channel(link):
    await client(LeaveChannelRequest(channel=link))