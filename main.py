import asyncio
import logging
from pyrogram import Client, idle, errors
from config import API_ID, API_HASH, BOT_TOKEN, validate_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    app = Client(
        name="tradingbot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
        plugins={"root": "BOT"},
        workers=10
    )

    try:
        await app.start()
        me = await app.get_me()
        logger.info(f"Bot started: @{me.username}")
        await idle()
    except errors.AuthKeyInvalid:
        logger.error("Invalid API credentials")
    except errors.AccessTokenInvalid:
        logger.error("Invalid bot token")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await app.stop()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())