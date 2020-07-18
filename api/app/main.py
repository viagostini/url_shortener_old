from fastapi import FastAPI
from pydantic import BaseModel

from urllib.parse import urlparse

from .shortlink import random_url

class Url(BaseModel):
    url: str


BASE_URL = 'http://short.vini/'

app = FastAPI()


db = {
    '4WeXc2T': 'https://github.com/viagostini'
}

@app.post('/')
async def create_shortlink(url: Url):
    new_url = random_url()
    db[new_url] = url.url
    return {'url': BASE_URL + new_url}
    
@app.get('/')
async def get_url(url: Url):
    shortlink = urlparse(url.url)[2][1:]
    return {'url': db.get(shortlink)}