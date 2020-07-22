import secrets, string

def random_shortlink(length: int = 7) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
