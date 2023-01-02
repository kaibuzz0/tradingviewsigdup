import asyncio
from pyrogram import Client, idle
from config import API_ID,API_HASH,BOT_TOKEN


async def main():
    CLI = Client(name='-',
                 bot_token=BOT_TOKEN,
                 api_id=API_ID,
                 api_hash=API_HASH,
                 in_memory=True,
                 plugins={"root": "BOT"},
                 workers=999)
    await CLI.start()
    print('BOT STARTED')
    await idle()


asyncio.run(main())
