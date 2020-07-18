import json
from urllib.parse import urlparse

import redis
from locust import HttpUser, between, task, events

shortlinks = ['1234567']

db = redis.Redis()

def clear_db():
    pipe = db.pipeline()
    for link in shortlinks:
        pipe.delete(link)
    pipe.execute()

class QuickstartUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @events.test_stop.add_listener
    def on_test_stop(**kwargs):
        print('Clearing DB entries!')
        clear_db()

    @task
    def create_post(self):
        headers = {
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip',
        }
        res = self.client.post('/', data=json.dumps({
            'url': 'https://github.com/viagostini'
        }), headers=headers, name='Create a new URL')

        # remember created links to cleanup after
        shortlink = urlparse(res.json()['url'])[2][1:]
        shortlinks.append(shortlink)

    @task(2)
    def get_url(self):
        self.client.get(f'/{shortlinks[-1]}', allow_redirects=False)
