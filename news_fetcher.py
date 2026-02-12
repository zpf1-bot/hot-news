import json
import os
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def fetch_url(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_hacker_news():
    json_data = fetch_url("https://hacker-news.firebaseio.com/v0/topstories.json")
    if not json_data:
        return []
    
    ids = json.loads(json_data)[:10]
    news = []
    for i, story_id in enumerate(ids):
        item = fetch_url(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        if item:
            data = json.loads(item)
            news.append({
                'title': data.get('title', ''),
                'url': data.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                'source': 'Hacker News',
                'time': datetime.now().isoformat(),
                'heat': 1000 - i * 50,
                'category': 'tech'
            })
    return news

def fetch_all_news():
    print("Fetching news...")
    return parse_hacker_news()

def save_cache(news_data, cache_file='data/news_cache.json'):
    os.makedirs(os.path.dirname(cache_file) if os.path.dirname(cache_file) else '.', exist_ok=True)
    cache = {'news': news_data, 'updated_at': datetime.now().isoformat()}
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def load_cache(cache_file='data/news_cache.json'):
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'news': [], 'updated_at': None}

if __name__ == '__main__':
    news = fetch_all_news()
    print(f"Got {len(news)} news items")
    save_cache(news)
