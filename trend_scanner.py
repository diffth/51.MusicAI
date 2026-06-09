import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import datetime

class TrendScanner:
    def __init__(self):
        self.google_rss_url = "https://trends.google.com/trending/rss"
        self.namespaces = {
            'ht': 'http://www.google.com/trends/trendingsearches/trends'
        }

    def fetch_google_trends(self, geo='US'):
        """구글 트렌드 RSS 피드로부터 인기 검색어 및 트래픽을 추출합니다."""
        url = f"{self.google_rss_url}?geo={geo}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            items = root.findall('.//item')
            
            trends = []
            for item in items:
                title = item.find('title').text
                approx_traffic = item.find('ht:approx_traffic', self.namespaces)
                traffic_str = approx_traffic.text if approx_traffic is not None else "0"
                
                # 트래픽 문자열 정수형 변환 (예: "50,000+" -> 50000)
                traffic_val = int(traffic_str.replace('+', '').replace(',', '').strip())
                
                description = item.find('description').text
                pub_date = item.find('pubDate').text
                
                # 뉴스 링크 수집
                news_items = []
                news_list = item.findall('ht:news_item', self.namespaces)
                for news in news_list:
                    news_title = news.find('ht:news_item_title', self.namespaces)
                    news_url = news.find('ht:news_item_url', self.namespaces)
                    if news_title is not None and news_url is not None:
                        news_items.append({
                            'title': news_title.text,
                            'url': news_url.text
                        })
                
                trends.append({
                    'keyword': title,
                    'traffic': traffic_val,
                    'traffic_display': traffic_str,
                    'description': description,
                    'pub_date': pub_date,
                    'news': news_items
                })
            
            # 트래픽 순으로 정렬
            trends.sort(key=lambda x: x['traffic'], reverse=True)
            return trends
            
        except Exception as e:
            print(f"[ERROR] 구글 트렌드 획득 실패 ({geo}): {str(e)}")
            return []

    def scan_and_save(self, geo_list=['US', 'KR'], output_file='trends.json'):
        """다양한 지역의 트렌드를 분석하고 파일로 저장합니다."""
        results = {
            'scanned_at': datetime.datetime.now().isoformat(),
            'trends': {}
        }
        
        for geo in geo_list:
            print(f"[INFO] '{geo}' 지역의 트렌드 데이터를 수집 중입니다...")
            trends = self.fetch_google_trends(geo)
            results['trends'][geo] = trends
            print(f"[SUCCESS] '{geo}' 트렌드 수집 완료. ({len(trends)}개 항목)")
            
        # 결과 저장
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f"[SUCCESS] 트렌드 분석 리포트가 '{output_file}'에 저장되었습니다.")
            return results
        except Exception as e:
            print(f"[ERROR] 파일 저장 실패: {str(e)}")
            return None

if __name__ == "__main__":
    scanner = TrendScanner()
    scanner.scan_and_save()
