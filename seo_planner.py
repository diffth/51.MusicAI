import json
import os

class SEOPlanner:
    def __init__(self, plan_file='visual_plan.json'):
        self.plan_file = plan_file

    def generate_seo_metadata(self):
        """기획된 비주얼 컨셉에 맞춰 유튜브 알고리즘을 극대화할 SEO 메타데이터를 자동 생성합니다."""
        if not os.path.exists(self.plan_file):
            print(f"[ERROR] '{self.plan_file}' 파일이 존재하지 않습니다.")
            return None
            
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                plan = json.load(f)
        except Exception as e:
            print(f"[ERROR] 기획 정보 로드 실패: {str(e)}")
            return None
            
        keyword = plan.get('keyword', 'Music')
        concept = plan.get('concept', 'Chill Beats')
        image_prompt = plan.get('image_prompt', '')
        
        # 1. 멱살잡이 제목(Title) 기획
        # CTR을 극대화하는 자극적이고 트렌디한 포맷
        title_alternatives = [
            f"🔥 {concept.upper()} | 1-Hour Energetic Cyberpunk Beats for Peak Performance 🎧",
            f"⚡ {keyword.upper()} VIBES - Intense Gym & Workout Cyberpunk Playlist (2026)",
            f"🔴 RUN FAST - {concept} | Aggressive Synthwave / Cyberpunk Workout Music Mix"
        ]
        selected_title = title_alternatives[0]
        
        # 2. 알고리즘 최적화 설명란(Description) 작성
        # (기획 의도, AI 프롬프트 투명 공개 포함)
        description = (
            f"Welcome to MusicAI World. Today we present an exclusive cyberpunk playlist inspired by '{keyword}'.\n\n"
            f"🎵 Track Concept: {concept}\n"
            f"🚀 This high-energy mix is carefully curated to boost your focus, intensity, and motivation "
            f"during workout sessions or deep focus coding.\n\n"
            f"=========================================\n"
            f"🤖 [TRANSPARENT AI PRODUCTION INFO]\n"
            f"We transparently disclose the AI generation settings and prompts used for this content:\n\n"
            f"🎨 Thumbnail Image Prompt:\n"
            f"\"{image_prompt}\"\n\n"
            f"🎹 Music Synthesis Directive:\n"
            f"\"Fast-paced darksynth, driving bassline, retro futuristic synthesizer leads, 120BPM, epic motivation.\"\n"
            f"=========================================\n\n"
            f"Enjoying the track? Don't forget to Like, Subscribe, and leave your thoughts below!\n\n"
            f"#synthwave #cyberpunk #workoutmusic #musicai #bgm"
        )
        
        # 3. 해시태그 및 태그(Tags) 추출
        tags = [
            keyword.lower(),
            "cyberpunk music",
            "synthwave workout",
            "darksynth mix",
            "musicai",
            "focus beats",
            "study music",
            "gaming bgm",
            "workout motivation"
        ]
        
        seo_plan = {
            'title': selected_title,
            'description': description,
            'tags': tags,
            'title_options': title_alternatives
        }
        
        # 결과 저장
        try:
            with open('seo_plan.json', 'w', encoding='utf-8') as f:
                json.dump(seo_plan, f, ensure_ascii=False, indent=4)
            print("[SUCCESS] SEO plan saved to 'seo_plan.json'.")
            try:
                print(f" -> Title: {selected_title}")
            except UnicodeEncodeError:
                print(f" -> Title: [Emoji stripped] {selected_title.encode('ascii', 'ignore').decode('ascii')}")
            return seo_plan
        except Exception as e:
            print(f"[ERROR] SEO plan save failed: {str(e)}")
            return None

if __name__ == "__main__":
    planner = SEOPlanner()
    planner.generate_seo_metadata()
