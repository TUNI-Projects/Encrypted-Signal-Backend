import re
import base64


def check_password(password):
    alphanumeric_regex = r'[0-9a-zA-Z]+'
    special_char_regex = r'[!@#$%^&*(),.?:{}|<>]'

    if len(password) >= 8 and len(password) <= 32 and re.match(alphanumeric_regex, password) and not re.match(special_char_regex, password):
        return True
    # password is invalid
    return False


def padding(password: bytes):
    if len(password) < 32:
        password = password + b'\0' * (32 - len(password))
    elif len(password) > 32:
        password = password[:32]
    return password
