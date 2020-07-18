import json

from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def create_post(self):
        headers = {
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip',
        }
        self.client.post('/', data=json.dumps({
            'url': 'https://github.com/viagostini'
        }), headers=headers, name='Create a new URL')

    @task(2)
    def get_url(self):
        self.client.get('/', data=json.dumps({
            'url': 'http://short.vini/4WeXc2T'
        }))