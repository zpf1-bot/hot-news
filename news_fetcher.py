import json
import os
import re
from datetime import datetime
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError, HTTPError

def fetch_url(url, headers=None):
    try:
        req = Request(url, headers=headers or {'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except (URLError, HTTPError, Exception) as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_github_trending():
    html = fetch_url("https://github.com/trending?since=daily")
    if not html:
        return []
    
    news = []
    pattern = r'<a class="Link" href="([^"]+)"[^>]*>([^<]+)</a>'
    for i, match in enumerate(re.finditer(pattern, html)):
        news.append({
            'title': match.group(2).strip(),
            'url': 'https://github.com' + match.group(1),
            'source': 'GitHub',
            'time': datetime.now().isoformat(),
            'heat': 1000 - i * 50,
            'category': 'tech'
        })
        if i >= 9:
            break
    return news

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

def parse_product_hunt():
    html = fetch_url("https://www.producthunt.com/")
    if not html:
        return []
    
    news = []
    pattern = r'<a[^>]*href="/posts/([^"]+)"[^>]*>([^<]+)</a>'
    for i, match in enumerate(re.finditer(pattern, html)):
        news.append({
            'title': match.group(2).strip(),
            'url': 'https://www.producthunt.com/posts/' + match.group(1),
            'source': 'Product Hunt',
            'time': datetime.now().isoformat(),
            'heat': 1000 - i * 50,
            'category': 'tech'
        })
        if i >= 9:
            break
    return news

def fetch_all_news():
    all_news = []
    sources = [
        ('GitHub Trending', parse_github_trending),
        ('Hacker News', parse_hacker_news),
        ('Product Hunt', parse_product_hunt),
    ]
    
    for name, fetcher in sources:
        try:
            result = fetcher()
            if result:
                all_news.extend(result)
            print(f"Fetched {len(result)} items from {name}")
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    
    unique_news = []
    seen_urls = set()
    for item in all_news:
        if isinstance(item, dict) and item.get('url'):
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_news.append(item)
    
    unique_news.sort(key=lambda x: x.get('heat', 0), reverse=True)
    return unique_news

def save_cache(news_data, cache_file='data/news_cache.json'):
    os.makedirs(os.path.dirname(cache_file) if os.path.dirname(cache_file) else '.', exist_ok=True)
    cache = {
        'news': news_data,
        'updated_at': datetime.now().isoformat()
    }
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def load_cache(cache_file='data/news_cache.json'):
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'news': [], 'updated_at': None}

if __name__ == '__main__':
    news = fetch_all_news()
    save_cache(news)
    print(f"Saved {len(news)} news items to cache")
