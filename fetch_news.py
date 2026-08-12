import os
import json
import feedparser

# 抓取新聞 RSS
def get_news():
    # 使用中央社即時新聞 RSS
    rss_url = "https://www.cna.com.tw/rss/aall.xml"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    # 抓取前 10 則新聞
    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link
        
        # 簡單標題過濾與處理
        news_list.append({
            "cat": "即時新聞",
            "type": "event",
            "source": "中央社",
            "time": "最新",
            "summary": f"📌 {title}",
            "url": link
        })
    return news_list

if __name__ == "__main__":
    try:
        data = get_news()
        # 強制寫入 news.json 檔案
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Successfully written to news.json")
    except Exception as e:
        print(f"Error: {e}")
