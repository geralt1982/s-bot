#!/usr/bin/env python3
"""
Telegram Gifts Monitor Bot - Интенсивные уведомления
Основано на https://github.com/arynyklas/tg_gifts_notifier
Модифицировано для интенсивных уведомлений и развертывания на Render
"""

import asyncio
import os
import threading
from flask import Flask
from detector import main as detector_main
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask веб-сервер для предотвращения засыпания на Render
app = Flask(__name__)

@app.route('/')
def health_check():
    """Проверка работоспособности бота"""
    return {
        "status": "running",
        "bot": "Telegram Gifts Monitor",
        "message": "Bot is monitoring @gifts_detector"
    }

@app.route('/ping')
def ping():
    """Endpoint для автопинга"""
    return "Bot is alive!"

@app.route('/status')
def status():
    """Статус бота"""
    return {
        "status": "active",
        "monitoring": "gifts_detector",
        "notifications": "enabled"
    }

def run_flask():
    """Запуск Flask сервера в отдельном потоке"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

async def run_bot():
    """Запуск основного бота"""
    try:
        logger.info("🚀 Запуск Telegram Gifts Monitor Bot...")
        from detector import main as detector_main
await detector_main()
    except Exception as e:
        logger.error(f"❌ Ошибка в работе бота: {e}")
        # Перезапуск через 30 секунд
        await asyncio.sleep(30)
        await run_bot()

def main():
    """Главная функция - запуск веб-сервера и бота"""
    logger.info("🔧 Инициализация системы...")
    
    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Веб-сервер запущен")
    
    # Запуск основного бота
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
