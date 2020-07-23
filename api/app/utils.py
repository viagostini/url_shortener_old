import secrets, string


async def unique_random_shortlink(collection):
    url = random_shortlink()
    while _ := await collection.find_one({ "_id": url }):
        url = random_shortlink()
    return url

def random_shortlink(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
