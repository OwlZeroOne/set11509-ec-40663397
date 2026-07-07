import random
import unicodedata

from typing import Any
from faker import Faker
from faker.providers import BaseProvider


class DomainProvider(BaseProvider):
    __domains = [
        "Technology",
        "Energy",
        "Finance",
        "Healthcare",
        "Real Estate",
        "Industries"
    ]
    def domain(self) -> str:
        return random.choice(self.__domains)


class TradingRecordProvider(BaseProvider):
    def record(self) -> int:
        return random.randint(100, 10000)


class RatingProvider(BaseProvider):
    def rating(self) -> int:
        return random.randint(1, 5)


class PriceProvider(BaseProvider):
    def price(self) -> float:
        return round(random.uniform(20.0, 60.0), 2)


def generate_brokers(locales: list[str], count: int) -> list[dict[str, Any]]:
    brokers = []
    for _ in range(count):
        fk = Faker([random.choice(locales)])
        fk.add_provider(TradingRecordProvider)
        fk.add_provider(RatingProvider)
        fk.add_provider(PriceProvider)
        fk.add_provider(DomainProvider)

        name = f"{fk.first_name()} {fk.last_name()}"
        broker = {
            'name': name,
            'email': f"{_username_from_name(name)}@{fk.domain_name()}",
            'phone': random.choice([fk.phone_number(), None]),
            'domain': fk.domain(),
            'trading_record': fk.record(),
            'rating': fk.rating(),
            'price': fk.price()
        }
        brokers.append(broker)
    return brokers


def _username_from_name(name: str) -> str:
    try:
        _, forename, surname = name.split(" ")
    except ValueError:
        forename, surname = name.split(" ")
    return f"{_remove_accents(forename[0])}{surname[:7]}"


def _remove_accents(text: str) -> str:
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')


