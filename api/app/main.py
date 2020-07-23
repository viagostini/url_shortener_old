from datetime import datetime


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from . import database


app = FastAPI()


BASE_URL = 'http://localhost:8000/'

class UrlCreate(BaseModel):
    url: str

class UrlCreateCustom(UrlCreate):
    shortlink: str

@app.post('/')
async def create_shortlink(req: UrlCreate):
    res = await database.create_shortlink(req.url)
    return {'shortlink': BASE_URL + res}
    
@app.post('/custom')
async def create_custom_shortlink(req: UrlCreateCustom):
    res = await database.create_shortlink(req.url, req.shortlink)
    if not res:
        raise HTTPException(status_code=400, detail='Shortlink already in use')
    return {'shortlink': BASE_URL + res}

@app.get('/{shortlink}')
async def get_url_from_shortlink(shortlink: str):
    url = await database.get_url(shortlink)
    return RedirectResponse(url=url['url'] if url else '/')
