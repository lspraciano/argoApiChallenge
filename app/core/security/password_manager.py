import random
import re
from typing import Optional

from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password(
        password: str,
        hash_password: str
) -> bool:
    return CRIPTO.verify(password, hash_password)


def generate_hash_password(
        password: str
) -> str:
    return CRIPTO.hash(password)


async def generate_password(
        length: int = 8
) -> str:
    if type(length) is not int or length is None:
        length = 8

    char_seq: str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[]^_`{|}~"
    password: str = ""

    for i in range(length):
        random_char: str = random.choice(char_seq)
        password += random_char

    list_pass: list = list(password)
    random.shuffle(list_pass)
    output_password: str = ''.join(list_pass)
    return output_password


def validate_password_string(
        password: str
) -> bool:
    if not password or type(password) is not str:
        return False

    regex: re = re.compile(
        r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@$%^&*]).{8,}$'
    )
    result: Optional[str] = re.fullmatch(regex, password)
    if result:
        return True
    else:
        return False
