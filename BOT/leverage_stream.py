from pyrogram import Client, filters
import logging
from config import SPOT_CHANNEL, LEVERAGE_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.chat([LEVERAGE_CHANNEL]))
async def leverage_handler(client, message):
    """
    Listen to leverage channel for close signals (❌)
    Forward close signal to spot channel
    """
    try:
        if not message.text:
            return
            
        if '❌' not in message.text:
            return
            
        lines = message.text.split('\n')
        if not lines or ':' not in lines[0]:
            logger.warning(f"Invalid close message format: {message.text[:50]}")
            return
            
        ticker = lines[0].split(':')[1].strip()
        restyle = f'CLOSE {ticker}'
        
        await client.send_message(
            chat_id=SPOT_CHANNEL,
            text=restyle
        )
        logger.info(f"Close signal forwarded: {ticker}")
        
    except Exception as e:
        logger.error(f"Error in leverage_handler: {e}")