from datetime import datetime


from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from . import database
from .shortlink import random_shortlink


app = FastAPI()

shortlinks = database.shortlinks_collection()


BASE_URL = 'http://localhost:8000/'

class Url(BaseModel):
    url: str

async def unique_random_shortlink():
    url = random_shortlink()
    while _ := await shortlinks.find_one({ "_id": url }):
        url = random_shortlink()
    return url


@app.post('/')
async def create_shortlink(url: Url):
    shortlink = await unique_random_shortlink()
    await shortlinks.insert_one({
        "_id": shortlink,
        "url": url.url,
        "createdAt": datetime.now()
    })
    return {'url': BASE_URL + shortlink}
    
@app.get('/{shortlink}')
async def get_url_from_shortlink(shortlink: str):
    res = await shortlinks.find_one({ "_id": shortlink })
    return RedirectResponse(url=res['url'] if res else '/')
