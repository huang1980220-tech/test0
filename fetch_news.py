import urllib.request
import xml.etree.ElementTree as ET
import json
import re

# 抓取 RSS 即時新聞來源（中央社焦點新聞）
RSS_URL = "https://www.cna.com.tw/rss/aall.aspx"

def fetch_real_news():
    news_list = []
    try:
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        for item in root.findall('.//item')[:10]: # 抓最新 10 篇實體新聞
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else '#'
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else '即時'
            description = item.find('description').text if item.find('description') is not None else ''
            
            # 清理 HTML 標籤
            clean_desc = re.sub('<[^<]+?>', '', description).strip()
            if len(clean_desc) > 80:
                clean_desc = clean_desc[:80] + "..."
                
            # 去除常見的命理/廣告關鍵字
            if any(bad_word in title for bad_word in ['星座', '運勢', '紫微', '廣編']):
                continue

            news_list.append({
                "cat": "焦點",
                "source": "中央社",
                "time": pubDate[17:22] if len(pubDate) > 22 else "即時",
                "summary": f"📌 {title}",
                "bullets": [f"📄 {clean_desc}"] if clean_desc else [],
                "url": link
            })
    except Exception as e:
        print(f"抓取失敗: {e}")
        
    # 如果抓取有資料，存成 news.json
    if news_list:
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print("成功更新真實新聞列表！")

if __name__ == "__main__":
    fetch_real_news()
