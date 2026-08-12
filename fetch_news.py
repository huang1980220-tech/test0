import os
import json
import feedparser

def get_news():
    rss_url = "https://www.cna.com.tw/rss/aall.xml"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    for entry in feed.entries[:10]:
        news_list.append({
            "title": entry.title,
            "url": entry.link,
            "source": "中央社",
            "time": "最新"
        })
    return news_list

if __name__ == "__main__":
    try:
        data = get_news()
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Successfully written to news.json")
    except Exception as e:
        print(f"Error: {e}")
