import logging
import os
from pathlib import Path

# Константы
WORK_DIRPATH = Path(__file__).parent

# Основные настройки из переменных окружения
SESSION_NAME = os.getenv("SESSION_NAME", "gifts_monitor")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

# Токены ботов - читаем из BOT_TOKENS (как в Render)
BOT_TOKENS = [
    token.strip()
    for token in os.getenv("BOT_TOKENS", "").split(",")
    if token.strip()
]

CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "1.0"))
CHECK_UPGRADES_PER_CYCLE = float(os.getenv("CHECK_UPGRADES_PER_CYCLE", "2.0"))

DATA_FILEPATH = WORK_DIRPATH / "star_gifts.json"
DATA_SAVER_DELAY = float(os.getenv("DATA_SAVER_DELAY", "2.0"))

NOTIFY_CHAT_ID = int(os.getenv("NOTIFY_CHAT_ID", "0"))
NOTIFY_UPGRADES_CHAT_ID = int(os.getenv("NOTIFY_UPGRADES_CHAT_ID", "0")) if os.getenv("NOTIFY_UPGRADES_CHAT_ID") else None

NOTIFY_AFTER_STICKER_DELAY = float(os.getenv("NOTIFY_AFTER_STICKER_DELAY", "1.0"))
NOTIFY_AFTER_TEXT_DELAY = float(os.getenv("NOTIFY_AFTER_TEXT_DELAY", "2.0"))

# Важно! Эта переменная нужна для импорта в detector.py
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Настройки логирования
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.INFO

HTTP_REQUEST_TIMEOUT = float(os.getenv("HTTP_REQUEST_TIMEOUT", "20.0"))

# Тексты уведомлений (оригинальные из config.example.py)
NOTIFY_TEXT = """{title}

№ {number} (<code>{id}</code>)

{total_amount}{available_amount}{sold_out}

💎 Price: {price} ⭐️

♻️ Convert price: {convert_price} ⭐️

"""

NOTIFY_TEXT_TITLES = {
    True: "🔥 A new limited gift has appeared",
    False: "❄️ A new gift has appeared"
}

NOTIFY_TEXT_TOTAL_AMOUNT = "\n🎯 Total amount: {total_amount}"
NOTIFY_TEXT_AVAILABLE_AMOUNT = "\n❓ Available amount: {available_amount} ({same_str}{available_percentage}%, updated at {updated_datetime} UTC)\n"
NOTIFY_TEXT_SOLD_OUT = "\n⏰ Completely sold out in {sold_out}\n"
NOTIFY_UPGRADES_TEXT = "Gift is upgradable! (<code>{id}</code>)"

def validate_config():
    """Проверка конфигурации"""
    errors = []
    
    if not API_ID or API_ID == 0:
        errors.append("API_ID не задан")
    
    if not API_HASH:
        errors.append("API_HASH не задан")
    
    if not BOT_TOKENS:
        errors.append("BOT_TOKENS не заданы")
    
    if not NOTIFY_CHAT_ID or NOTIFY_CHAT_ID == 0:
        errors.append("NOTIFY_CHAT_ID не задан")
    
    if errors:
        raise ValueError(f"Ошибки конфигурации: {', '.join(errors)}")
    
    return True
