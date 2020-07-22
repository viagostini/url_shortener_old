from datetime import timedelta

import redis
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from .shortlink import random_url


app = FastAPI()

db = redis.Redis()


BASE_URL = 'http://localhost:8000/'

class Url(BaseModel):
    url: str

async def get_unique_random_url():
    url = random_url()
    while db.get(url):
        url = random_url()
    return url

@app.post('/')
async def create_shortlink(url: Url):
    new_url = await get_unique_random_url()
    db.setex(new_url, timedelta(days=730), url.url)
    return {'url': BASE_URL + new_url}
    
@app.get('/{shortlink}')
async def get_url_from_shortlink(shortlink: str):
    url = db.get(shortlink)

    if not url:
        return RedirectResponse(url='/')
    
    return RedirectResponse(url=url.decode('utf-8'))
