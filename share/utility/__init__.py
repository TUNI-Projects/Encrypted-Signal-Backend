import re


def check_password(password):
    alphanumeric_regex = r'[0-9a-zA-Z]+'
    special_char_regex = r'[!@#$%^&*(),.?:{}|<>]'
    
    if len(password) >= 8 and re.match(alphanumeric_regex, password) and not re.match(special_char_regex, password):
        return True
    # password is invalid
    return False
