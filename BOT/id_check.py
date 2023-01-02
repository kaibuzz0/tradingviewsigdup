from pyrogram import Client,filters


@Client.on_message(filters.command(['start']))
async def id_check(client,message):
    print(message.chat.id)
    await message.reply(message.chat.id)