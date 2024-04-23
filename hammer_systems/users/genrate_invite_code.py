import random
import string


def create_invite_code(values):
    code = string.ascii_letters + string.digits
    return ''.join(random.choice(code) for _ in range(values))
