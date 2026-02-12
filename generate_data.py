import json
import os
from datetime import datetime
from news_fetcher import fetch_all

OUTPUT_DIR = 'data'

KEYWORDS = {
    'finance': ['stock', 'market', 'crypto', 'bitcoin', 'trading', 'invest', 'bank', 'econom', 'price', 'fund', 'coin', 'ether', 'eth ', 'dollar', 'fed', 'rate', 'inflation'],
    'social': ['news', 'politics', 'government', 'world', 'country', 'people', 'city', 'police', 'court', 'law', 'health', 'virus', 'vaccine', 'climate', 'environment', 'election']
}

def categorize_news(news_item):
    title = news_item.get('title', '').lower()
    source = news_item.get('source', '').lower()
    
    for keyword in KEYWORDS['finance']:
        if keyword in title:
            return 'finance'
    
    for keyword in KEYWORDS['social']:
        if keyword in title:
            return 'social'
    
    if 'github' in source:
        return 'tech'
    return 'tech'

def filter_by_category(news_list, category):
    if category == 'all':
        return news_list
    return [item for item in news_list if categorize_news(item) == category]

def generate_category_json(all_news, category, output_path):
    filtered = filter_by_category(all_news, category)
    top_news = sorted(filtered, key=lambda x: x.get('heat', 0), reverse=True)[:10]
    
    cache_data = {
        'news': top_news,
        'updated_at': datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {output_path}: {len(top_news)} items ({category})")

def main():
    print("Fetching news data...")
    all_news = fetch_all()
    
    print(f"Total fetched: {len(all_news)}")
    
    categories = ['all', 'tech', 'finance', 'social']
    for cat in categories:
        output_path = os.path.join(OUTPUT_DIR, f'{cat}.json')
        generate_category_json(all_news, cat, output_path)
    
    print("\nDone!")

if __name__ == '__main__':
    main()
