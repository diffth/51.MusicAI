import os
from dotenv import load_dotenv

# 로컬 .env 파일의 환경 변수를 메모리에 로드합니다.
load_dotenv()

class Config:
    # YouTube API 설정
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE", "client_secrets.json")
    
    # 구글 시트 연동 설정
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
    
    # 비디오 합성 설정
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY", "./output")
    
    # 채널 기본 설정
    DEFAULT_TAGS = ["MusicAI", "Lofi", "Relaxing", "AI-Generated"]

    @classmethod
    def validate(cls):
        """필수 설정값들이 제대로 설정되어 있는지 확인합니다."""
        missing = []
        if not cls.YOUTUBE_API_KEY:
            missing.append("YOUTUBE_API_KEY")
        if not os.path.exists(cls.CLIENT_SECRETS_FILE):
            missing.append(f"CLIENT_SECRETS_FILE (Path not found: {cls.CLIENT_SECRETS_FILE})")
            
        if missing:
            print(f"[Luna Warning] 누락된 설정 값이 감지되었습니다: {', '.join(missing)}")
            return False
        return True

if __name__ == "__main__":
    print("[Luna Config] 현재 설정을 검증합니다...")
    Config.validate()
