from pyrogram import Client, filters
import re
import logging
from config import (
    SPOT_CHANNEL, LEVERAGE_CHANNEL, 
    DEFAULT_LEVERAGE, DEFAULT_POSITION_SIZE
)

logger = logging.getLogger(__name__)

# Pattern matchers for different alert formats
BUY_PATTERN = re.compile(r'buy\s+(\w+)', re.IGNORECASE)
SELL_PATTERN = re.compile(r'sell\s+(\w+)', re.IGNORECASE)
LONG_PATTERN = re.compile(r'long', re.IGNORECASE)


def parse_signal(message_text: str) -> dict | None:
    """
    Parse trading signal from various formats.
    Supports: TradingView, custom buy/sell, and legacy formats.
    """
    result = {
        'pair': None,
        'side': None,
        'exchange': None,
        'entry': None,
        'targets': [],
        'stop_loss': None
    }
    
    lines = message_text.split('\n')
    text_lower = message_text.lower()
    
    # Check for simple buy/sell format
    buy_match = BUY_PATTERN.search(message_text)
    sell_match = SELL_PATTERN.search(message_text)
    
    if buy_match:
        result['side'] = 'LONG'
        result['pair'] = buy_match.group(1).upper()
    elif sell_match:
        result['side'] = 'SHORT'
        result['pair'] = sell_match.group(1).upper()
    
    # TradingView format parsing (more robust)
    for line in lines:
        line_lower = line.lower()
        
        # Pair detection
        if 'pair' in line_lower or 'symbol' in line_lower:
            if ':' in line:
                result['pair'] = line.split(':', 1)[1].strip().upper()
        
        # Exchange detection
        if 'exchange' in line_lower:
            if ':' in line:
                result['exchange'] = line.split(':', 1)[1].strip()
        
        # Entry detection
        if 'entry' in line_lower or 'buy' in line_lower:
            numbers = re.findall(r'[\d.]+', line)
            if numbers:
                result['entry'] = numbers[0]
        
        # Target detection
        if 'target' in line_lower or 'tp' in line_lower or 'take profit' in line_lower:
            numbers = re.findall(r'[\d.]+', line)
            if numbers:
                result['targets'].extend(numbers)
        
        # Stop loss detection
        if 'stop' in line_lower or 'sl' in line_lower:
            numbers = re.findall(r'[\d.]+', line)
            if numbers:
                result['stop_loss'] = numbers[0]
    
    # Validate minimum required data
    if result['pair'] and result['side']:
        return result
    
    # Check for legacy 🟩 format (long signals)
    if '🟩' in message_text and LONG_PATTERN.search(message_text):
        return parse_legacy_format(message_text)
    
    return None


def parse_legacy_format(text: str) -> dict | None:
    """Parse legacy TradingView alert format"""
    try:
        lines = text.split('\n')
        if len(lines) < 2:
            return None
            
        first_line = lines[0].strip()
        parts = first_line.split()
        if len(parts) >= 2:
            return {
                'pair': parts[1],
                'side': 'LONG',
                'exchange': None,
                'entry': None,
                'targets': [],
                'stop_loss': None
            }
    except Exception:
        pass
    return None


def format_cornix(signal: dict, leverage: int, position_size: float) -> str:
    """Format signal for Cornix auto-trading"""
    exchange = signal.get('exchange') or 'Binance'
    entry = signal.get('entry') or 'Market'
    
    targets = signal.get('targets', [])
    target_str = targets[0] if targets else 'TBD'
    sl = signal.get('stop_loss') or 'TBD'
    
    return f"""Coin: {signal['pair']}
Direction: {signal['side']}
Exchange: {exchange}
Leverage: {leverage}x
Entry: {entry}
Position Size: {position_size}%

Target 1: {target_str}
Stop Loss: {sl}"""


def format_threecommas(signal: dict, leverage: int) -> str:
    """Format signal for 3Commas"""
    return f"""{signal['pair']} {signal['side']}
Leverage: {leverage}x
Entry: {signal.get('entry', 'Market')}
SL: {signal.get('stop_loss', 'N/A')}
TP: {signal.get('targets', ['N/A'])[0] if signal.get('targets') else 'N/A'}"""


@Client.on_message(filters.chat([SPOT_CHANNEL]))
async def spot_handler(client, message):
    """
    Process spot channel signals and forward to leverage channel
    """
    try:
        if not message.text:
            return
        
        logger.info(f"Received message in spot channel: {message.text[:100]}")
        
        # Parse the signal
        signal = parse_signal(message.text)
        
        if not signal:
            logger.debug("Message didn't match any signal pattern")
            return
        
        logger.info(f"Parsed signal: {signal}")
        
        # Send simplified close signal to leverage channel
        close_msg = f"{signal['pair']} close {signal['side']}"
        await client.send_message(
            chat_id=LEVERAGE_CHANNEL,
            text=close_msg
        )
        logger.info(f"Close signal sent: {close_msg}")
        
        # Only send detailed signal for LONG positions
        if signal['side'] != 'LONG':
            return
        
        # Format for Cornix (can add more formats)
        detailed_signal = format_cornix(signal, DEFAULT_LEVERAGE, DEFAULT_POSITION_SIZE)
        
        await client.send_message(
            chat_id=LEVERAGE_CHANNEL,
            text=detailed_signal
        )
        logger.info(f"Detailed signal sent to leverage channel")
        
    except Exception as e:
        logger.error(f"Error in spot_handler: {e}", exc_info=True)