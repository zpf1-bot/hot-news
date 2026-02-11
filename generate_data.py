import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from news_fetcher import fetch_all_news

OUTPUT_DIR = 'data'
CATEGORIES = {
    'tech': ['AI', 'LLM', 'GPT', 'GitHub', 'Product Hunt', '36kr', 'Hacker News'],
    'finance': ['股票', '加密货币', '华尔街见闻', 'Finance', 'Market', 'A股', '比特币'],
    'social': ['微博热搜', '腾讯新闻', 'Weibo']
}

SOURCE_CATEGORY_MAP = {
    'hackernews': 'tech',
    'github': 'tech',
    'producthunt': 'tech',
    '36kr': 'tech',
    'weibo': 'social',
    'tencent': 'social',
    'wallstreetcn': 'finance',
    'v2ex': 'tech'
}

def categorize_news(news_item):
    source = news_item.get('source', '').lower()
    title = news_item.get('title', '')
    
    for cat_key, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title.lower():
                return cat_key
    
    return SOURCE_CATEGORY_MAP.get(source, 'tech')

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
    
    print(f"Generated {output_path} with {len(top_news)} items")

def main():
    print("Fetching news data...")
    all_news = fetch_all_news()
    
    print(f"Total news fetched: {len(all_news)}")
    
    categories = ['all', 'tech', 'finance', 'social']
    for cat in categories:
        output_path = os.path.join(OUTPUT_DIR, f'{cat}.json')
        generate_category_json(all_news, cat, output_path)
    
    print("\nAll data files generated successfully!")

if __name__ == '__main__':
    main()
