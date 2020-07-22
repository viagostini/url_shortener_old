import os
from datetime import datetime

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from .shortlink import random_shortlink


app = FastAPI()

load_dotenv()
mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
database_name = os.getenv("DATABASE_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.gws4q.gcp.mongodb.net/{database_name}?retryWrites=true&w=majority")
mongo_db = client['URLShortener']
shortlinks = mongo_db.shortlinks


BASE_URL = 'http://localhost:8000/'

class Url(BaseModel):
    url: str

async def get_unique_random_shortlink():
    url = random_shortlink()
    while shortlinks.find_one({ "_id": url }):
        url = random_shortlink()
    return url

@app.post('/')
async def create_shortlink(url: Url):
    new_url = await get_unique_random_shortlink()
    await shortlinks.insert_one({
        "_id": new_url,
        "url": url.url,
        "createdAt": datetime.now()
    })
    return {'url': BASE_URL + new_url}
    
@app.get('/{shortlink}')
async def get_url_from_shortlink(shortlink: str):
    url = await shortlinks.find_one({ "_id": shortlink })
    if not url['url']:
        return RedirectResponse(url='/')
    return RedirectResponse(url=url['url'])
