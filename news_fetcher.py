import json
import os
from datetime import datetime, timedelta
from urllib.request import urlopen, Request

def fetch(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return urlopen(req, timeout=8).read().decode('utf-8')
    except:
        return None

def hacker_news():
    data = fetch("https://hacker-news.firebaseio.com/v0/topstories.json")
    if not data:
        return []
    ids = json.loads(data)[:10]
    news = []
    for i, sid in enumerate(ids):
        item = fetch(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
        if item:
            d = json.loads(item)
            url = d.get('url', f'https://news.ycombinator.com/item?id={sid}')
            news.append({
                'title': d.get('title', ''),
                'url': url,
                'source': 'Hacker News',
                'time': datetime.now().isoformat(),
                'heat': 1000 - i * 50,
                'category': 'tech'
            })
    return news

def github_trending():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    data = fetch(f"https://api.github.com/search/repositories?q=created:>{yesterday}&sort=stars&order=desc")
    if not data:
        return []
    try:
        items = json.loads(data).get('items', [])[:10]
        return [{
            'title': i['full_name'],
            'url': i['html_url'],
            'source': 'GitHub',
            'time': datetime.now().isoformat(),
            'heat': i.get('stargazers_count', 0),
            'category': 'tech'
        } for i in items]
    except:
        return []

def fetch_all():
    news = []
    news.extend(hacker_news())
    print(f"HN: {len(news)}")
    news.extend(github_trending())
    print(f"GitHub: {len(news)}")
    
    seen = set()
    unique = []
    for n in news:
        url = n.get('url', '')
        if url and url not in seen:
            seen.add(url)
            unique.append(n)
    
    unique.sort(key=lambda x: x.get('heat', 0), reverse=True)
    return unique

def save(news):
    cache = {'news': news, 'updated_at': datetime.now().isoformat()}
    with open('data/news_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    n = fetch_all()
    print(f"Total: {len(n)}")
    save(n)
