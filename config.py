import os
from dotenv import load_dotenv

load_dotenv()

# Channel IDs
SPOT_CHANNEL: int = int(os.getenv("SPOT_CHANNEL_ID", "-10101"))
LEVERAGE_CHANNEL: int = int(os.getenv("LEVERAGE_CHANNEL_ID", "-10101"))
DCA_CHANNEL: int = int(os.getenv("DCA_CHANNEL_ID", "-10101"))

# Trading Settings
DEFAULT_LEVERAGE: int = int(os.getenv("DEFAULT_LEVERAGE", "5"))
DEFAULT_POSITION_SIZE: float = float(os.getenv("DEFAULT_POSITION_SIZE", "2.0"))

# Bot Settings
API_ID: int = int(os.getenv("API_ID", "0"))
API_HASH: str = os.getenv("API_HASH", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

# Validate required settings
def validate_config():
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if missing:
        raise ValueError(f"Missing required config: {', '.join(missing)}")
    return True