import feedparser
import json
import re

# 黑名單：過濾星座命理與廣告業配
BLACK_LIST = ['星座', '運勢', '算命', '紫微', '塔羅', '生肖', '風水', '廣編特輯', '業配', '特別企劃']

# 即時新聞來源 (中央社、ETtoday等)
RSS_URLS = [
    'https://news.google.com/rss?hl=zh-TW&gl=TW&ceid=TW:zh-Hant',
    'https://www.cna.com.tw/rss/aall.aspx'
]

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

def process_rss():
    news_list = []
    
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            link = entry.link
            
            # 過濾黑名單
            if any(bad_word in title for bad_word in BLACK_LIST):
                continue
                
            # 清理標題來源標籤 (例如： - 中央社)
            clean_title = title.split(' - ')[0] if ' - ' in title else title
            
            news_list.append({
                'cat': '即時',
                'source': '焦點新聞',
                'time': '最新',
                'summary': f"📌 {clean_title}",
                'url': link
            })
            
            if len(news_list) >= 10:
                break
        if len(news_list) >= 10:
            break

    # 存成 news.json 給網頁讀取
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    process_rss()
