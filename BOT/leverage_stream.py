from pyrogram import Client, filters
from config import spot_channel, leverage_channel


@Client.on_message(filters.chat([leverage_channel]))
async def id_check(client, message):
  """
    Stream speicified leverage_channel
    """
  if '❌' not in message.text:
    return
  ticker = (message.text).split('\n')[0].split(':')[1]
  restyle = f'CLOSE {ticker}'
  await client.send_message(chat_id=spot_channel, text=restyle)
