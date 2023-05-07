# MentionBot script
# made by asmpro
# date: 25/4/2023
# TG:@asmprotk

from telethon import TelegramClient, events

api_id = 0
api_hash = '0'
bot_token = '0'

MENTION_LIMIT = 4

client = TelegramClient('mention_bot', api_id,
                        api_hash).start(bot_token=bot_token)

important_members = {}


async def is_admin(chat_id, user_id):
    chat = await client.get_entity(chat_id)
    permissions = await client.get_permissions(chat, user_id)
    return permissions.is_admin


@client.on(events.NewMessage(pattern=r'/mention|الكل'))
async def handle_mention(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not await is_admin(chat_id, user_id):
        await event.respond('Sorry, only admins can use this command.')
        return
    members = await client.get_participants(chat_id)
    mention_list = []
    for member in members:
        if member.username:
            mention_list.append('@' + member.username)
    for i in range(0, len(mention_list), MENTION_LIMIT):
        mention_str = ' '.join(mention_list[i:i+MENTION_LIMIT])
        await client.send_message(chat_id, mention_str)


@client.on(events.NewMessage(pattern=r'/important|مهم'))
async def handle_important(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if user_id in important_members:
        await event.respond('You are already on the important list.')
        return
    important_members[user_id] = True
    await event.respond('You have been added to the important list.')


@client.on(events.NewMessage(pattern=r'/unimportant|غير مهم'))
async def handle_unimportant(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if user_id not in important_members:
        await event.respond('You are not on the important list.')
        return
    del important_members[user_id]
    await event.respond('You have been removed from the important list.')


@client.on(events.NewMessage(pattern=r'/mimportant|المهمين'))
async def handle_mention_important(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not await is_admin(chat_id, user_id):
        await event.respond('Sorry, only admins can use this command.')
        return
    mention_list = []
    for member_id in important_members:
        member = await client.get_entity(member_id)
        if member.username:
            mention_list.append('@' + member.username)
    if not mention_list:
        await event.respond('No important members found.')
        return
    for i in range(0, len(mention_list), MENTION_LIMIT):
        mention_str = ' '.join(mention_list[i:i+MENTION_LIMIT])
        await client.send_message(chat_id, mention_str)


client.run_until_disconnected()
