import os
from datetime import datetime
from operator import itemgetter

import motor.motor_asyncio
from dotenv import load_dotenv

from .utils import unique_random_shortlink

def get_user_credentials():
    load_dotenv()
    return {
        "user": os.getenv("MONGO_USER"),
        "password": os.getenv("MONGO_PASS"),
        "database": os.getenv("DATABASE_NAME")
    }


def shortlinks_collection():
    user, password, database = itemgetter('user', 'password', 'database') \
                                    (get_user_credentials())

    server = (
        f"mongodb+srv://{user}:{password}"
        f"@cluster0.gws4q.gcp.mongodb.net/"
        f"{database}?retryWrites=true&w=majority"
    )
    client = motor.motor_asyncio.AsyncIOMotorClient(server)
    mongo_db = client['URLShortener']
    return mongo_db.shortlinks




async def create_shortlink(url, custom_shortlink=None):
    shortlinks = shortlinks_collection()
    new_shortlink = custom_shortlink
    if not custom_shortlink:
        new_shortlink = await unique_random_shortlink(shortlinks)
    else:
        if await shortlinks.find_one({ "_id": custom_shortlink }):
            return None
    await shortlinks.insert_one({
        "_id": new_shortlink,
        "url": url,
        "createdAt": datetime.now()
    })
    return new_shortlink

async def get_url(shortlink):
    shortlinks = shortlinks_collection()
    res = await shortlinks.find_one({ "_id": shortlink })
    return res