from abc import ABC, abstractmethod
from typing import List

from app.digest.digest import Digest


class DeliveryChannel(ABC):
    @abstractmethod
    async def deliver(self, digest: Digest) -> None:
        pass


class DigestPublisher:
    def __init__(self):
        self._channels: List[DeliveryChannel] = []

    def subscribe(self, channel: DeliveryChannel) -> None:
        self._channels.append(channel)

    async def publish(self, digest: Digest) -> None:
        for channel in self._channels:
            await channel.deliver(digest)
