# Патерни

## Adapter (структурний)

Кожен формат стрічки записує новини по-своєму. Адаптер перекладає свій формат у `Article`, тому решта програми не знає, звідки прийшла новина.

```mermaid
classDiagram
    class FeedSource {
        <<abstract>>
        +fetch() list~Article~
    }
    class RssSource {
        -_url
        -_name
        +fetch() list~Article~
        -_download() bytes
        -_parse(data) list~Article~
    }
    class AtomSource {
        <<план>>
    }
    class JsonFeedSource {
        <<план>>
    }
    class Article
    FeedSource <|-- RssSource
    FeedSource <|-- AtomSource
    FeedSource <|-- JsonFeedSource
    RssSource ..> Article : створює
```

## Observer (поведінковий)

Дайджест не знає, куди його шлють. Канали підписуються на `DigestPublisher` і отримують готовий дайджест. Новий канал (email, HTML) додається без зміни інших класів.

```mermaid
classDiagram
    class DigestPublisher {
        -_channels
        +subscribe(channel)
        +publish(digest)
    }
    class DeliveryChannel {
        <<abstract>>
        +deliver(digest)
    }
    class ConsoleChannel {
        +deliver(digest)
    }
    class TelegramChannel {
        -_token
        -_chat_id
        +deliver(digest)
    }
    DigestPublisher o-- DeliveryChannel
    DeliveryChannel <|-- ConsoleChannel
    DeliveryChannel <|-- TelegramChannel
```

## Composite (структурний, план)

Правила І / АБО / НЕ складаються з інших правил. `RuleEngine` працює з будь-яким правилом через `matches`, не знаючи, просте воно чи складене. Зараз є `KeywordRule`, складені правила будуть наступними.

```mermaid
classDiagram
    class Rule {
        <<abstract>>
        +matches(article) bool
    }
    class KeywordRule {
        -keyword_
        +matches(article) bool
    }
    class AndRule {
        <<план>>
        -rules
        +matches(article) bool
    }
    class OrRule {
        <<план>>
        -rules
        +matches(article) bool
    }
    class NotRule {
        <<план>>
        -rule
        +matches(article) bool
    }
    class RuleEngine {
        +filter(articles, rule) list~id~
    }
    Rule <|-- KeywordRule
    Rule <|-- AndRule
    Rule <|-- OrRule
    Rule <|-- NotRule
    AndRule o-- Rule
    OrRule o-- Rule
    NotRule o-- Rule
    RuleEngine ..> Rule
```

## Decorator (структурний, план)

`CachedSource` обгортає будь-яке джерело: зберігає новини і віддає збережені, коли немає мережі. Саме джерело при цьому не змінюється.

```mermaid
classDiagram
    class FeedSource {
        <<abstract>>
        +fetch() list~Article~
    }
    class RssSource
    class CachedSource {
        <<план>>
        -inner: FeedSource
        -cache: ArticleCache
        +fetch() list~Article~
    }
    class ArticleCache {
        <<план>>
        +save(articles)
        +load(source) list~Article~
    }
    FeedSource <|-- RssSource
    FeedSource <|-- CachedSource
    CachedSource o-- FeedSource
    CachedSource --> ArticleCache
```
