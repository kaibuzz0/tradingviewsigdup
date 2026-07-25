from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import (
    SPOT_CHANNEL, LEVERAGE_CHANNEL, DCA_CHANNEL,
    DEFAULT_LEVERAGE, DEFAULT_POSITION_SIZE
)

logger = logging.getLogger(__name__)

# User configuration storage (in-memory, can be replaced with Redis/DB)
user_configs = {}


@Client.on_message(filters.command(['config', 'settings']))
async def config_menu(client, message):
    """Show configuration menu"""
    user_id = message.from_user.id
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Set Channels", callback_data="set_channels")],
        [InlineKeyboardButton("Trading Settings", callback_data="trading_settings")],
        [InlineKeyboardButton("Service Format", callback_data="service_format")],
        [InlineKeyboardButton("View Current Config", callback_data="view_config")],
    ])
    
    await message.reply(
        "⚙️ **Trading Bot Configuration**\n\n"
        "Select an option to configure:",
        reply_markup=keyboard
    )


@Client.on_callback_query()
async def handle_callback(client, callback):
    """Handle menu callbacks"""
    data = callback.data
    user_id = callback.from_user.id
    
    if data == "set_channels":
        await callback.message.edit_text(
            "📡 **Channel Configuration**\n\n"
            "Use these commands to set channels:\n"
            "`/set_spot <channel_id>` - Spot signals channel\n"
            "`/set_leverage <channel_id>` - Leverage signals channel\n"
            "`/set_dca <channel_id>` - DCA signals channel\n\n"
            "Get channel ID by sending `/id` in any channel",
        )
    
    elif data == "trading_settings":
        await callback.message.edit_text(
            "💰 **Trading Settings**\n\n"
            f"Current:\n"
            f"Leverage: {DEFAULT_LEVERAGE}x\n"
            f"Position Size: {DEFAULT_POSITION_SIZE}%\n\n"
            "Commands:\n"
            "`/set_leverage <amount>` - Set default leverage\n"
            "`/set_position <percent>` - Set position size %",
        )
    
    elif data == "service_format":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Cornix", callback_data="fmt_cornix")],
            [InlineKeyboardButton("3Commas", callback_data="fmt_3commas")],
            [InlineKeyboardButton("Custom", callback_data="fmt_custom")],
        ])
        await callback.message.edit_text(
            "📋 **Service Format**\n\n"
            "Select your preferred format:",
            reply_markup=keyboard
        )
    
    elif data == "view_config":
        config_text = (
            "📋 **Current Configuration**\n\n"
            f"Spot Channel: `{SPOT_CHANNEL}`\n"
            f"Leverage Channel: `{LEVERAGE_CHANNEL}`\n"
            f"DCA Channel: `{DCA_CHANNEL}`\n\n"
            f"Default Leverage: {DEFAULT_LEVERAGE}x\n"
            f"Position Size: {DEFAULT_POSITION_SIZE}%\n\n"
            f"User Config: {user_configs.get(user_id, 'Not set')}"
        )
        await callback.message.edit_text(config_text)
    
    elif data.startswith("fmt_"):
        fmt = data.replace("fmt_", "")
        if user_id not in user_configs:
            user_configs[user_id] = {}
        user_configs[user_id]['format'] = fmt
        await callback.message.edit_text(f"✅ Format set to: **{fmt}**")
    
    await callback.answer()


@Client.on_message(filters.command(['set_leverage']))
async def set_leverage_cmd(client, message):
    """Set custom leverage for user"""
    try:
        leverage = int(message.command[1])
        user_id = message.from_user.id
        if user_id not in user_configs:
            user_configs[user_id] = {}
        user_configs[user_id]['leverage'] = leverage
        await message.reply(f"✅ Leverage set to {leverage}x")
    except (IndexError, ValueError):
        await message.reply("Usage: `/set_leverage <amount>` (e.g., `/set_leverage 10`)")


@Client.on_message(filters.command(['set_position']))
async def set_position_cmd(client, message):
    """Set custom position size for user"""
    try:
        size = float(message.command[1])
        user_id = message.from_user.id
        if user_id not in user_configs:
            user_configs[user_id] = {}
        user_configs[user_id]['position_size'] = size
        await message.reply(f"✅ Position size set to {size}%")
    except (IndexError, ValueError):
        await message.reply("Usage: `/set_position <percent>` (e.g., `/set_position 5`)")


@Client.on_message(filters.command(['help', 'commands']))
async def help_cmd(client, message):
    """Show help message"""
    help_text = """
🤖 **Trading Bot Commands**

**Configuration:**
`/start` or `/id` - Get channel ID
`/config` or `/settings` - Open config menu
`/set_leverage <amount>` - Set leverage
`/set_position <percent>` - Set position size

**Info:**
`/help` - Show this message
`/view_config` - View current settings

**Signal Formats Supported:**
- `buy BTCUSDT` / `sell BTCUSDT`
- TradingView alerts
- Custom formatted alerts

**Auto-processing:**
- 🟩 Long signals → Forwarded with leverage
- ❌ Close signals → Forwarded to close positions
"""
    await message.reply(help_text)