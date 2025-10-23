import os
import requests

BASE = os.getenv('SMOKE_BASE', 'http://web:8000')

def get(path):
    url = BASE + path
    r = requests.get(url, timeout=10)
    print(f"GET {path} -> {r.status_code}")
    if r.ok:
        try:
            data = r.json()
            if isinstance(data, list):
                print(f"  items: {len(data)}")
            elif isinstance(data, dict):
                print(f"  keys: {list(data.keys())[:5]}")
        except Exception:
            print("  (non-JSON response)")
    return r

if __name__ == '__main__':
    get('/api/sports/categories/')
    get('/api/sports/leagues/')
    get('/api/sports/games/upcoming/')
