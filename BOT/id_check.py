from pyrogram import Client, filters
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command(['start', 'id']))
async def id_check(client, message):
    """Get chat ID - useful for configuring channels"""
    try:
        chat_id = message.chat.id
        chat_type = message.chat.type
        logger.info(f"ID check from {chat_type} chat: {chat_id}")
        await message.reply(f"Chat ID: `{chat_id}`\nType: {chat_type}")
    except Exception as e:
        logger.error(f"Error in id_check: {e}")
        await message.reply("Error getting chat ID")