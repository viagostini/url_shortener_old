import os
from operator import itemgetter

import motor.motor_asyncio
from dotenv import load_dotenv

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
