# TradingView Signal Duplicator

Telegram bot for processing, restyling, and forwarding trading signals between channels.

## Features

- **Multi-format Signal Parsing**: Supports TradingView, custom buy/sell alerts
- **Channel Forwarding**: Auto-forward signals between spot and leverage channels
- **Signal Restyling**: Convert to Cornix, 3Commas, or custom formats
- **Interactive Menu**: Configure channels and settings via Telegram commands
- **Robust Error Handling**: Graceful handling of malformed messages

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your Telegram API credentials and channel IDs
```

3. **Get channel IDs:**
- Add bot to channels
- Send `/id` in each channel
- Copy the IDs to `.env`

4. **Run:**
```bash
python main.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start`, `/id` | Get current chat ID |
| `/config`, `/settings` | Configuration menu |
| `/set_leverage <amount>` | Set default leverage |
| `/set_position <percent>` | Set position size |
| `/help` | Show help message |

## Supported Signal Formats

### Simple Buy/Sell
```
buy BTCUSDT
sell ETHUSDT
```

### TradingView Format
```
Pair: BTCUSDT
Exchange: Binance
Entry: 45000
Target 1: 46000
Stop Loss: 44000
```

## Configuration

Edit `.env` file:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

SPOT_CHANNEL_ID=-1001234567890
LEVERAGE_CHANNEL_ID=-1001234567891
DCA_CHANNEL_ID=-1001234567892

DEFAULT_LEVERAGE=5
DEFAULT_POSITION_SIZE=2.0
```

## Architecture

```
main.py          → Bot entry point
config.py        → Environment configuration
BOT/
├── id_check.py      → ID retrieval
├── spot_stream.py   → Spot signal processing
├── leverage_stream.py → Leverage signal processing
└── menu.py          → Interactive config menu
```

## License

GNU GPL v3.0