import asyncio
import os

from app.bridge.cpp_rule_client import CppRuleClient
from app.delivery.base import DigestPublisher
from app.delivery.console_channel import ConsoleChannel
from app.digest.digest import DigestBuilder
from app.sources.rss_source import RssSource


def main() -> None:
    feed_url = os.getenv("FEED_URL", "https://dou.ua/feed/")
    keyword = os.getenv("KEYWORD", "python")
    cpp_url = os.getenv("CPP_URL", "http://127.0.0.1:8080")

    articles = RssSource(feed_url, "DOU").fetch()
    print(f"Завантажено новин: {len(articles)}")

    matched = CppRuleClient(cpp_url).filter(articles, keyword)
    print(f"Підійшло під «{keyword}»: {len(matched)}\n")

    digest = DigestBuilder().build(matched, keyword)

    publisher = DigestPublisher()
    publisher.subscribe(ConsoleChannel())

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        from app.delivery.telegram_channel import TelegramChannel
        publisher.subscribe(TelegramChannel(token, chat_id))

    asyncio.run(publisher.publish(digest))


if __name__ == "__main__":
    main()
