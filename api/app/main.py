from datetime import datetime


from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from . import database


app = FastAPI()


BASE_URL = 'http://localhost:8000/'

class Url(BaseModel):
    url: str

@app.post('/')
async def create_shortlink(url: Url):
    shortlink = await database.create_shortlink(url.url)
    return {'url': BASE_URL + shortlink}
    
@app.get('/{shortlink}')
async def get_url_from_shortlink(shortlink: str):
    url = await database.get_url(shortlink)
    return RedirectResponse(url=url if url else '/')
