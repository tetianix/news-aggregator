from aiogram import Bot

from app.delivery.base import DeliveryChannel
from app.digest.digest import Digest


class TelegramChannel(DeliveryChannel):
    def __init__(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id

    async def deliver(self, digest: Digest) -> None:
        bot = Bot(token=self._token)
        try:
            await bot.send_message(chat_id=self._chat_id, text=digest.to_text())
        finally:
            await bot.session.close()
