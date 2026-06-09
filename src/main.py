import os
import sys
from config import Config
from trend_scanner import TrendScanner
from video_generator.py (가져오기 형식을 위해 generator로 구성)

# 실제로는 import 구문을 맞춘다.
from trend_scanner import TrendScanner
from video_generator import VideoGenerator
from youtube_publisher import YouTubePublisher

def run_luna_automation():
    print("==========================================================")
    print("🤖 에이전트 루나 - 음악 및 비주얼 유튜브 채널 무인 자동화 시작")
    print("==========================================================")
    
    # 1. 설정 유효성 검증
    if not Config.validate():
        print("[Luna Error] 초기 설정에 필요한 API 키 혹은 인증 파일이 부족합니다.")
        print("[Luna Action] 로컬에 .env 파일을 만들고 필요한 변수를 입력해 주세요.")
        
    # 2. 트렌드 스캔 및 키워드 확보
    print("\n--- [1단계] 트렌드 스캐닝 및 키워드 선정 ---")
    scanner = TrendScanner()
    target_keyword = scanner.get_best_keyword()
    print(f"최종 콘텐츠 키워드: {target_keyword}")

    # 3. AI 비주얼 및 오디오 생성 기획
    print("\n--- [2단계] 이미지/오디오 에셋 준비 ---")
    # 이미지 생성: Antigravity의 generate_image 툴 등을 내부에서 활용
    # 오디오 생성: 로열티 프리 라이브러리 결합 또는 Suno API 등
    image_file = "mock_background.png"
    audio_file = "mock_music.mp3"
    
    # 임시 목업 파일이 존재한다고 가정
    if not os.path.exists(image_file):
        with open(image_file, "w") as f:
            f.write("mock image data")
    if not os.path.exists(audio_file):
        with open(audio_file, "w") as f:
            f.write("mock audio data")

    # 4. 비디오 컴파일링 (FFmpeg)
    print("\n--- [3단계] 고해상도 비디오 합성 ---")
    output_video = "output_video.mp4"
    generator = VideoGenerator(ffmpeg_path=Config.FFMPEG_PATH)
    generator.compile_video(image_file, audio_file, output_video)

    # 5. 유튜브 예약 업로드
    print("\n--- [4단계] 유튜브 예약 발행 (음악 카테고리) ---")
    publisher = YouTubePublisher(client_secrets_path=Config.CLIENT_SECRETS_FILE)
    
    title = f"[{target_keyword}] 마음이 편안해지는 AI 연주곡 🎧"
    description = (
        f"에이전트 루나가 실시간 트렌드 키워드 '{target_keyword}' 분석을 기반으로 제작한 고해상도 힐링 음악 콘텐츠입니다.\n\n"
        "■ AI 기획 의도 및 프롬프트:\n"
        " - visual prompt: lofi art style, pastel tones, cozy room\n"
        " - music style: chill lofi beats with soft piano melody"
    )
    
    publisher.authenticate()
    publisher.upload_video(
        file_path=output_video,
        title=title,
        description=description,
        tags=Config.DEFAULT_TAGS + [target_keyword]
    )

    print("\n==========================================================")
    print("🎉 에이전트 루나가 오늘 하루의 자동화 사이클을 완료했습니다!")
    print("==========================================================")

if __name__ == "__main__":
    run_luna_automation()
