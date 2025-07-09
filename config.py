"""
Конфигурация для Telegram Gifts Monitor Bot
Настройки для интенсивных уведомлений и мониторинга
"""

import os
import logging
from pathlib import Path

# Базовые настройки Telegram API
SESSION_NAME = os.getenv("SESSION_NAME", "gifts_monitor")
API_ID = int(os.getenv("API_ID") or os.getenv("TELEGRAM_API_ID") or "0")
API_HASH = os.getenv("API_HASH") or os.getenv("TELEGRAM_API_HASH") or ""

# Токены ботов для отправки уведомлений
BOT_TOKENS = [
    token.strip()
    for token in (os.getenv("BOT_TOKENS") or os.getenv("BOT_TOKEN") or "").split(",")
    if token.strip()
]

# Настройки мониторинга
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "10.0"))  # секунд между проверками
CHECK_UPGRADES_PER_CYCLE = float(os.getenv("CHECK_UPGRADES_PER_CYCLE", "30.0"))  # проверка апгрейдов

# Чаты для уведомлений
NOTIFY_CHAT_ID = int(os.getenv("NOTIFY_CHAT_ID") or "0")  # Ваш chat_id
NOTIFY_UPGRADES_CHAT_ID = int(os.getenv("NOTIFY_UPGRADES_CHAT_ID") or "0") if os.getenv("NOTIFY_UPGRADES_CHAT_ID") else None

# Настройки интенсивных уведомлений
MAX_NOTIFICATIONS = int(os.getenv("MAX_NOTIFICATIONS", "50"))  # максимум уведомлений
NOTIFICATION_INTERVAL = float(os.getenv("NOTIFICATION_INTERVAL", "5.0"))  # секунд между уведомлениями
NOTIFY_AFTER_STICKER_DELAY = float(os.getenv("NOTIFY_AFTER_STICKER_DELAY", "2.0"))
NOTIFY_AFTER_TEXT_DELAY = float(os.getenv("NOTIFY_AFTER_TEXT_DELAY", "3.0"))

# Настройки файлов и логов
WORK_DIRPATH = Path(__file__).parent
DATA_FILEPATH = WORK_DIRPATH / "star_gifts.json"
DATA_SAVER_DELAY = float(os.getenv("DATA_SAVER_DELAY", "5.0"))

# Настройки логирования
CONSOLE_LOG_LEVEL = logging.INFO
FILE_LOG_LEVEL = logging.INFO
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# HTTP настройки
HTTP_REQUEST_TIMEOUT = float(os.getenv("HTTP_REQUEST_TIMEOUT", "30.0"))

# Тексты уведомлений
NOTIFY_TEXT = """
🚨 {title} 🚨

№ {number} (ID: <code>{id}</code>)

{total_amount}{available_amount}{sold_out}

💎 Цена: {price} ⭐️

♻️ Цена конвертации: {convert_price} ⭐️

⏰ ДЕЙСТВУЙ БЫСТРО!
"""

NOTIFY_TEXT_TITLES = {
    True: "🔥 НОВЫЙ ЛИМИТИРОВАННЫЙ ПОДАРОК",
    False: "❄️ НОВЫЙ ПОДАРОК"
}

NOTIFY_TEXT_TOTAL_AMOUNT = "\n🎯 Всего: {total_amount}"
NOTIFY_TEXT_AVAILABLE_AMOUNT = "\n❓ Доступно: {available_amount} ({same_str}{available_percentage}%, обновлено {updated_datetime})\n"
NOTIFY_TEXT_SOLD_OUT = "\n⏰ Распродано за {sold_out}\n"
NOTIFY_UPGRADES_TEXT = "🎁 Подарок можно апгрейдить! (ID: <code>{id}</code>)"
