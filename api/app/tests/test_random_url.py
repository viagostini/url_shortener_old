from ..shortlink import random_url


def test_random_url_length():
    for _ in range(10000):
        url = random_url()
        assert len(url) == 7

def test_random_url_isalnum():
    for _ in range(10000):
        url = random_url()
        assert url.isalnum()