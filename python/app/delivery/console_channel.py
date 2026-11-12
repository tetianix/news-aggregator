from app.delivery.base import DeliveryChannel
from app.digest.digest import Digest


class ConsoleChannel(DeliveryChannel):
    async def deliver(self, digest: Digest) -> None:
        print(digest.to_text())
