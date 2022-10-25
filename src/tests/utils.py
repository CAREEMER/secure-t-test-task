import random
from string import ascii_lowercase, digits


def generate_random_string(length: int = 10):
    return "".join([random.choice(ascii_lowercase + digits) for _ in range(length)])


def assert_values(d1: dict, d2: dict, keys: list[str]):
    for key in keys:
        assert d1[key] == d2[key]
