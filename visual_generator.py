import json
import os

class VisualGenerator:
    def __init__(self, trends_file='trends.json'):
        self.trends_file = trends_file

    def select_best_keyword(self):
        """trends.json에서 AI 음악 및 비주얼에 가장 적합한 키워드를 선별합니다."""
        if not os.path.exists(self.trends_file):
            return "SpaceX Cosmic Journey" # 기본 키워드 백업
            
        try:
            with open(self.trends_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # US 트렌드 추출
            us_trends = data.get('trends', {}).get('US', [])
            
            # 비주얼/음악적 영감을 주는 추천 키워드 매핑
            inspiration_keywords = ['space', 'warrior', 'belfast', 'hollywood', 'nets', 'celtics', 'tim walz']
            
            for trend in us_trends:
                kw = trend.get('keyword', '').lower()
                for inspire in inspiration_keywords:
                    if inspire in kw:
                        return trend.get('keyword')
                        
            # 매칭되는 것이 없을 시 첫 번째 트렌드 키워드 반환
            if us_trends:
                return us_trends[0].get('keyword')
        except Exception as e:
            print(f"[ERROR] 키워드 선별 중 오류 발생: {str(e)}")
            
        return "SpaceX"

    def design_visual_concept(self):
        """선별된 키워드를 기반으로 썸네일/비주얼 생성 프롬프트를 기획합니다."""
        keyword = self.select_best_keyword()
        print(f"[INFO] 선별된 트렌드 키워드: '{keyword}'")
        
        # 키워드별 무드 세팅
        kw_lower = keyword.lower()
        if 'space' in kw_lower:
            concept = "SpaceX Cosmic Synthwave Odyssey"
            mood = "Dreamy, futuristic, cosmic, epic, neon cyberpunk"
            prompt = (
                "Futuristic SpaceX Starship launching into a neon cyber-nebula, synthwave aesthetics, "
                "vibrant violet and cyan glowing lights, highly detailed cosmic sky with digital stars, "
                "8k resolution, cinematic lighting, retro-futurism style, perfect for a music album cover."
            )
        elif 'warrior' in kw_lower or 'celtics' in kw_lower or 'nets' in kw_lower:
            concept = "Epic Stadium Workout Beats"
            mood = "Energetic, powerful, high contrast, dramatic glow"
            prompt = (
                "A dramatic cyberpunk basketball court glowing with gold and purple laser lines under a dark stormy sky, "
                "an intense energetic vibe, epic particle effects, dynamic angle, high contrast, 8k resolution."
            )
        else:
            concept = "Lofi Hollywood Retro Nostalgia"
            mood = "Retro, nostalgic, cozy, warm light, cinema style"
            prompt = (
                "Cozy retro cinema front desk on a rainy night, glowing warm neon signs, Ryan Reynolds style classic movie poster on the wall, "
                "nostalgic chill lofi mood, soft lighting, highly detailed, anime aesthetic style."
            )
            
        visual_plan = {
            'keyword': keyword,
            'concept': concept,
            'mood': mood,
            'image_prompt': prompt,
            'thumbnail_filename': 'youtube_thumbnail.png'
        }
        
        with open('visual_plan.json', 'w', encoding='utf-8') as f:
            json.dump(visual_plan, f, ensure_ascii=False, indent=4)
            
        print(f"[SUCCESS] 비주얼 컨셉 기획 완료 및 'visual_plan.json'에 저장됨.")
        print(f" -> 컨셉: {concept}")
        print(f" -> 이미지 프롬프트: {prompt}")
        return visual_plan

if __name__ == "__main__":
    generator = VisualGenerator()
    generator.design_visual_concept()
