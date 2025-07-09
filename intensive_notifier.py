"""
Система интенсивных уведомлений для пробуждения пользователя
Отправляет множественные уведомления до остановки процесса
"""

import asyncio
import logging
from typing import Optional, Dict, Any
import os
from httpx import AsyncClient, TimeoutException
from itertools import cycle
import time

logger = logging.getLogger(__name__)

class IntensiveNotifier:
    """Класс для отправки интенсивных уведомлений"""
    
    def __init__(self, config):
        self.config = config
        self.is_active = False
        self.current_notifications = 0
        self.stop_event = asyncio.Event()
        
        # HTTP клиент для Bot API
        self.http_client = AsyncClient(
            base_url="https://api.telegram.org/",
            timeout=config.HTTP_REQUEST_TIMEOUT
        )
        
        # Циклический итератор по токенам ботов
        self.bot_tokens_cycle = cycle(config.BOT_TOKENS)
        
        # Базовые параметры запроса
        self.basic_request_data = {
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
    
    async def send_bot_request(self, method: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Отправка запроса к Bot API с ротацией токенов"""
        retries = len(self.config.BOT_TOKENS)
        
        for bot_token in self.bot_tokens_cycle:
            retries -= 1
            if retries < 0:
                break
                
            try:
                response = (await self.http_client.post(
                    f"/bot{bot_token}/{method}",
                    json=data
                )).json()
                
                if response.get("ok"):
                    return response.get("result")
                    
            except TimeoutException:
                logger.warning(f"Timeout при отправке {method}")
                continue
        
        logger.error(f"Не удалось отправить запрос {method}")
        return None
    
    async def send_wake_up_sticker(self, chat_id: int, sticker_data: bytes, filename: str) -> Optional[int]:
        """Отправка стикера для пробуждения"""
        try:
            # Используем первый доступный токен для загрузки стикера
            bot_token = next(self.bot_tokens_cycle)
            
            # Отправляем стикер через multipart/form-data
            files = {
                'sticker': (filename, sticker_data, 'application/octet-stream')
            }
            data = {
                'chat_id': str(chat_id)
            }
            
            response = await self.http_client.post(
                f"/bot{bot_token}/sendSticker",
                files=files,
                data=data
            )
            
            result = response.json()
            if result.get("ok"):
                return result["result"]["message_id"]
                
        except Exception as e:
            logger.error(f"Ошибка отправки стикера: {e}")
            
        return None
    
    async def send_intensive_notification(self, chat_id: int, message: str, notification_num: int) -> bool:
        """Отправка одного интенсивного уведомления"""
        
        # Создаем сообщение для пробуждения
        wake_up_message = f"""
🚨 ВНИМАНИЕ! НОВЫЙ ПОДАРОК #{notification_num}! 🚨

⏰ ВРЕМЯ: {time.strftime('%H:%M:%S')}
🎯 ДЕЙСТВУЙ БЫСТРО!

{message}

💥 ПРОСНИСЬ И ПОКУПАЙ! 💥
"""
        
        data = {
            "chat_id": chat_id,
            "text": wake_up_message,
            **self.basic_request_data
        }
        
        result = await self.send_bot_request("sendMessage", data)
        return result is not None
    
    async def start_intensive_notifications(self, chat_id: int, gift_message: str, sticker_data: bytes, sticker_filename: str):
        """Запуск интенсивных уведомлений"""
        if self.is_active:
            logger.warning("Уведомления уже активны")
            return
        
        self.is_active = True
        self.current_notifications = 0
        self.stop_event.clear()
        
        logger.info(f"🚨 НАЧИНАЮ ИНТЕНСИВНЫЕ УВЕДОМЛЕНИЯ! Максимум: {self.config.MAX_NOTIFICATIONS}")
        
        try:
            # Первый стикер для пробуждения
            sticker_msg_id = await self.send_wake_up_sticker(chat_id, sticker_data, sticker_filename)
            if sticker_msg_id:
                logger.info("📌 Стикер отправлен для пробуждения")
            
            # Задержка после стикера
            await asyncio.sleep(self.config.NOTIFY_AFTER_STICKER_DELAY)
            
            # Цикл интенсивных уведомлений
            while (self.current_notifications < self.config.MAX_NOTIFICATIONS and 
                   not self.stop_event.is_set()):
                
                self.current_notifications += 1
                
                # Отправляем уведомление
                success = await self.send_intensive_notification(
                    chat_id, 
                    gift_message, 
                    self.current_notifications
                )
                
                if success:
                    logger.info(f"📱 Уведомление #{self.current_notifications} отправлено")
                else:
                    logger.error(f"❌ Не удалось отправить уведомление #{self.current_notifications}")
                
                # Дополнительный стикер каждые 5 уведомлений
                if self.current_notifications % 5 == 0:
                    await self.send_wake_up_sticker(chat_id, sticker_data, sticker_filename)
                    logger.info(f"📌 Дополнительный стикер #{self.current_notifications//5}")
                
                # Задержка между уведомлениями
                await asyncio.sleep(self.config.NOTIFICATION_INTERVAL)
            
            if self.stop_event.is_set():
                logger.info(f"🛑 Уведомления остановлены вручную на #{self.current_notifications}")
            else:
                logger.info(f"✅ Отправлено максимальное количество уведомлений: {self.current_notifications}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка в интенсивных уведомлениях: {e}")
        finally:
            self.is_active = False
            self.current_notifications = 0
    
    def stop_notifications(self):
        """Остановка интенсивных уведомлений"""
        if self.is_active:
            self.stop_event.set()
            logger.info("🛑 Получен сигнал остановки уведомлений")
        else:
            logger.info("ℹ️ Уведомления не активны")
    
    def get_status(self) -> Dict[str, Any]:
        """Получение статуса уведомлений"""
        return {
            "is_active": self.is_active,
            "current_notifications": self.current_notifications,
            "max_notifications": self.config.MAX_NOTIFICATIONS,
            "interval": self.config.NOTIFICATION_INTERVAL
        }