import asyncio
import os

from app.bridge.cpp_rule_client import CppRuleClient
from app.config import config_path, load_config
from app.delivery.base import DigestPublisher
from app.delivery.console_channel import ConsoleChannel
from app.digest.digest import DigestBuilder
from app.sources.factory import SourceFactory
from app.sources.loader import SourceLoader


def main() -> None:
    config = load_config()
    keyword = os.getenv("KEYWORD", "python")
    cpp_url = os.getenv("CPP_URL", "http://127.0.0.1:8080")

    factory = SourceFactory()
    sources = [factory.create(item) for item in config.get("sources", [])]
    print(f"Конфіг: {config_path().name}, джерел: {len(sources)}")

    result = SourceLoader(sources).load()
    for name, error in result.errors.items():
        print(f"Не вдалося завантажити {name}: {error}")
    print(f"Завантажено новин: {len(result.articles)}")

    matched = CppRuleClient(cpp_url).filter(result.articles, keyword)
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
