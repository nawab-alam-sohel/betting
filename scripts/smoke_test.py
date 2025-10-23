import os
import requests

# Allow overriding the base URL; default works inside Docker network
BASE = os.getenv('SMOKE_BASE', 'http://web:8000')

ENDPOINTS = [
    '/api/payments/providers/',
    '/api/payments/initiate/',
    '/api/sports/categories/',
    '/api/sports/games/upcoming/',
    '/api/bets/me/',
]

for ep in ENDPOINTS:
    url = BASE + ep
    try:
        r = requests.get(url, timeout=5)
        print(ep, r.status_code)
    except Exception as e:
        print(ep, 'ERROR', e)
