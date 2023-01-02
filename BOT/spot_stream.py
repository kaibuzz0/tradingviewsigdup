from pyrogram import Client, filters
from config import spot_channel,leverage_channel,leverage_amount
import re




@Client.on_message(filters.chat([spot_channel]))
async def id_check(client, message):
    if '🟩' not in message.text:
        return
    ticker = (message.text).split('\n\n')[0].split("\n \n")[0].split()
    restyle = f'{ticker[0]} close {ticker[1]}'
    
    await client.send_message(chat_id=leverage_channel, text=restyle)

    if not bool(re.search('Long', message.text)):
        return
        
    rep = (message.text).split(':')


    spot_to_leverage_restyle = f"""
Pair :{rep[0].split(chr(10))[0]}
exchanges: {rep[1].split(chr(10))[0]}
Leverage : {leverage_amount}x
Entry : {rep[3].split(chr(10))[2].replace(' Buy ','')}
Amount: 2.0%

Target 1: {rep[4].split(chr(10))[2].split(' ')[2]}
Stop Loss : {rep[5].split(')')[1]}"""


    await client.send_message(chat_id=leverage_channel,
                              text=spot_to_leverage_restyle)
