import json
import os
import sys
import subprocess
from datetime import datetime

SKILL_PATH = os.path.expanduser('~/.agents/skills/news-aggregator-skill')
DATA_DIR = 'data'

def run_skill_script(source, limit=10, keyword=None, deep=True):
    cmd = [sys.executable, f'{SKILL_PATH}/scripts/fetch_news.py']
    cmd.extend(['--source', source])
    cmd.extend(['--limit', str(limit)])
    if deep:
        cmd.append('--deep')
    if keyword:
        cmd.extend(['--keyword', keyword])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_PATH)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running skill script for {source}: {e}")
    return []

def fetch_all_news():
    all_news = []
    sources = ['hackernews', 'github', 'weibo', '36kr', 'producthunt', 'tencent', 'wallstreetcn', 'v2ex']
    
    for source in sources:
        try:
            result = run_skill_script(source=source, limit=10, deep=True)
            if result:
                all_news.extend(result)
            print(f"Fetched {len(result) if result else 0} items from {source}")
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
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
