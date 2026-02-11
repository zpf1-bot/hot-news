from news_fetcher import fetch_all_news, save_cache

if __name__ == '__main__':
    news = fetch_all_news()
    save_cache(news)
    print(f"Successfully fetched and saved {len(news)} news items")
