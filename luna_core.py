import os
import json
import datetime
from trend_scanner import TrendScanner
from visual_generator import VisualGenerator
from seo_planner import SEOPlanner
from youtube_publisher import YouTubePublisher

class LunaCore:
    def __init__(self):
        self.scanner = TrendScanner()
        self.generator = VisualGenerator()
        self.seo_planner = SEOPlanner()
        self.publisher = YouTubePublisher()
        
    def execute_autopilot(self):
        """100% 무인 유튜브 채널 운영 파이프라인을 실시간 가동합니다."""
        print("==================================================")
        print("[LUNA MULTI-AGENT SYSTEM] START AUTOPILOT PIPELINE")
        print(f"Execution Time: {datetime.datetime.now().isoformat()}")
        print("==================================================")
        
        # Step 1: 트렌드 스캔
        print("\n[Step 1] 실시간 글로벌 트렌드 수집 및 데이터 스캔 진행...")
        self.scanner.scan_and_save(geo_list=['US', 'KR'])
        
        # Step 2: 비주얼 기획
        print("\n[Step 2] 트렌드 기반 비주얼 테마 및 생성 프롬프트 설계...")
        plan = self.generator.design_visual_concept()
        keyword = plan.get('keyword')
        concept = plan.get('concept')
        
        # Step 3: SEO 플랜
        print("\n[Step 3] 알고리즘 최적화 제목, 해시태그, 제작 프롬프트 포함 설명란 빌드...")
        self.seo_planner.generate_seo_metadata()
        
        # Step 4: 썸네일 이미지 파일 검증
        # 만약 youtube_thumbnail.png가 없으면 기본 썸네일 스켈레톤 처리를 하거나 경고
        thumbnail_file = 'youtube_thumbnail.png'
        if not os.path.exists(thumbnail_file):
            print(f"[WARN] 실물 썸네일 이미지 '{thumbnail_file}'가 감지되지 않았습니다.")
            print(" -> 루나 AI 에이전트 도구를 통해 이미지를 먼저 생성해 주십시오.")
            print(" -> 가상 업로드 진행을 위해 더미 파일을 임시 배치합니다.")
            with open(thumbnail_file, 'wb') as f:
                f.write(b"MOCK THUMBNAIL IMAGE BY LUNA")
        else:
            print(f"[SUCCESS] 루나 전용 AI 고화질 썸네일 '{thumbnail_file}' 실물 파일 매핑 완료.")
            
        # Step 5: 퍼블리싱 및 예약 등록 (Mock 모드 자동 대응 포함)
        print("\n[Step 4] 골든 타임 계산 및 유튜브 채널 예약 업로드 전송...")
        # 임시 최종 비디오 파일 경로
        video_file = 'output/final_video.mp4'
        success = self.publisher.publish_video(
            video_file_path=video_file,
            thumbnail_path=thumbnail_file,
            schedule_hours_later=4 # 4시간 뒤 골든 타임 예약
        )
        
        if success:
            print("\n==================================================")
            print("[SUCCESS] LUNA PIPELINE COMPLETED SUCCESSFULLY!")
            print("==================================================")
            
            # 최종 성공 결과 로드하여 간략 요약
            report_file = 'publish_report.json'
            if os.path.exists(report_file):
                with open(report_file, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                
                print(f" -> Status: {report.get('status')}")
                try:
                    print(f" -> Title: {report.get('video_title')}")
                except UnicodeEncodeError:
                    t = report.get('video_title', '')
                    print(f" -> Title: [Safe] {t.encode('ascii', 'ignore').decode('ascii')}")
                print(f" -> Scheduled: {report.get('scheduled_time')}")
            return True
        else:
            print("\n[FAIL] 루나 파이프라인 구동 중 오류가 발생했습니다. 로그를 확인하세요.")
            return False

if __name__ == "__main__":
    luna = LunaCore()
    luna.execute_autopilot()
