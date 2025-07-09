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

# Валидация конфигурации
def validate_config():
    """Проверка обязательных параметров конфигурации"""
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
        print(f"⚠️ Предупреждение: {', '.join(errors)}")
        return False
    
    return True

# Автоматическая валидация при импорте
if __name__ != "__main__":
    validate_config()
    async def main():
    """Основная функция для запуска мониторинга подарков"""
    try:
        # Проверяем конфигурацию
        if not validate_config():
            logger.error("Ошибка конфигурации. Проверьте переменные окружения.")
            return
        
        # Создаем клиент Pyrogram
        app = Client(
            name=SESSION_NAME,
            api_id=API_ID,
            api_hash=API_HASH,
            workdir=WORK_DIRPATH,
            in_memory=True  # Предотвращает EOF ошибки
        )
        
        logger.info("🚀 Запуск мониторинга подарков...")
        
        # Запускаем мониторинг
        update_gifts_queue = asyncio.Queue()
        
        # Запускаем задачи
        tasks = [
            asyncio.create_task(detector(
                app=app,
                new_gift_callback=partial(process_new_gift, app),
                update_gifts_queue=update_gifts_queue
            )),
            asyncio.create_task(process_update_gifts(update_gifts_queue)),
            asyncio.create_task(star_gifts_upgrades_checker(app))
        ]
        
        # Ждем выполнения всех задач
        await asyncio.gather(*tasks)
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        # Перезапуск через 30 секунд
        await asyncio.sleep(30)
        await main()

if __name__ == "__main__":
    asyncio.run(main())
