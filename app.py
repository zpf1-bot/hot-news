import json
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

CACHE_FILE = 'data/news_cache.json'
CATEGORIES = {
    'tech': ['AI', 'LLM', 'GPT', 'GitHub', 'Product Hunt', '36kr'],
    'finance': ['股票', '加密货币', '华尔街见闻', 'Finance', 'Market'],
    'social': ['微博热搜', '腾讯新闻', 'Weibo'],
    'comprehensive': ['V2EX', '36kr']
}

SOURCE_CATEGORY_MAP = {
    'hackernews': 'tech',
    'github': 'tech',
    'producthunt': 'tech',
    '36kr': 'comprehensive',
    'weibo': 'social',
    'tencent': 'social',
    'wallstreetcn': 'finance',
    'v2ex': 'comprehensive'
}

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'news': [], 'updated_at': None}

def save_cache(news_data):
    cache = {'news': news_data, 'updated_at': datetime.now().isoformat()}
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def categorize_news(news_item):
    source = news_item.get('source', '').lower()
    title = news_item.get('title', '')
    
    for cat_key, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title.lower():
                return cat_key
    
    return SOURCE_CATEGORY_MAP.get(source, 'comprehensive')

def filter_news_by_category(news_list, category):
    if category == 'all':
        return news_list
    return [item for item in news_list if categorize_news(item) == category]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<category>')
def category_page(category):
    if category not in CATEGORIES and category != 'all':
        category = 'comprehensive'
    return render_template('category.html', category=category)

@app.route('/api/news')
def get_news():
    cache = load_cache()
    category = request.args.get('category', 'all')
    
    news = cache.get('news', [])
    filtered_news = filter_news_by_category(news, category)
    top_news = sorted(filtered_news, key=lambda x: x.get('heat', 0), reverse=True)[:10]
    
    return jsonify({
        'news': top_news,
        'updated_at': cache.get('updated_at'),
        'category': category
    })

@app.route('/api/news/<int:news_id>')
def get_news_detail(news_id):
    cache = load_cache()
    news_list = cache.get('news', [])
    
    if 0 <= news_id < len(news_list):
        return jsonify(news_list[news_id])
    return jsonify({'error': 'News not found'}), 404

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    try:
        from news_fetcher import fetch_all_news, save_cache
        all_news = fetch_all_news()
        save_cache(all_news)
        
        return jsonify({
            'success': True, 
            'count': len(all_news),
            'updated_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
