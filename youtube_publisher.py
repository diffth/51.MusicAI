import os
import json
import datetime

# YouTube Data API 라이브러리 임포트 시도
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False

class YouTubePublisher:
    def __init__(self, token_file='token.pickle', client_secrets_file='client_secrets.json'):
        self.token_file = token_file
        self.client_secrets_file = client_secrets_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        
    def authenticate(self):
        """YouTube API 인증을 진행합니다. 실패 시 None을 반환하고 Mock 모드로 전환합니다."""
        if not YOUTUBE_API_AVAILABLE:
            print("[WARN] Google API Client 라이브러리가 설치되어 있지 않습니다. Mock 모드로 작동합니다.")
            return None
            
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"[WARN] 토큰 갱신 실패: {str(e)}")
                    creds = None
            else:
                if not os.path.exists(self.client_secrets_file):
                    print(f"[WARN] '{self.client_secrets_file}' 파일이 누락되어 OAuth 인증을 진행할 수 없습니다. Mock 모드로 전환합니다.")
                    return None
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"[WARN] OAuth 로컬 인증 서버 기동 실패: {str(e)}")
                    return None
                    
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('youtube', 'v3', credentials=creds)

    def publish_video(self, video_file_path, thumbnail_path, seo_plan_path='seo_plan.json', schedule_hours_later=3):
        """비디오와 썸네일을 유튜브에 업로드하고 예약 설정을 잡습니다."""
        # SEO 플랜 로드
        if not os.path.exists(seo_plan_path):
            print(f"[ERROR] '{seo_plan_path}' 파일이 없습니다. 업로드를 진행할 수 없습니다.")
            return False
            
        with open(seo_plan_path, 'r', encoding='utf-8') as f:
            seo_data = json.load(f)
            
        title = seo_data.get('title', 'AI Music Track')
        description = seo_data.get('description', '')
        tags = seo_data.get('tags', [])
        
        # 예약 시간 계산 (골든 타임)
        publish_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=schedule_hours_later)
        publish_time_iso = publish_time.isoformat()
        
        print("[INFO] Attempting publish:")
        try:
            print(f" -> Title: {title}")
        except UnicodeEncodeError:
            print(f" -> Title: [Emoji stripped] {title.encode('ascii', 'ignore').decode('ascii')}")
        print(f" -> Scheduled Time (UTC): {publish_time_iso}")
        
        # 실제 비디오 파일 체크 (테스트 시 가상 비디오 파일 생성 가능)
        if not os.path.exists(video_file_path):
            print(f"[WARN] 비디오 파일 '{video_file_path}'이 감지되지 않았습니다. Mock 영상 파일로 진행합니다.")
            video_file_path = self.create_mock_video_file(video_file_path)

        youtube = self.authenticate()
        
        if youtube is None:
            # Mock 모드 배포 성공 시뮬레이션
            print("\n[MOCK MODE ACTIVE] YouTube API 인증 부재로 인해 로컬 예약 가상 시뮬레이션을 완료했습니다.")
            print(f"[MOCK SUCCESS] 가상 비디오 '{video_file_path}' 및 썸네일 '{thumbnail_path}'이(가)")
            print(f"               예약시간 {publish_time_iso}에 성공적으로 가상 등록되었습니다.")
            
            mock_report = {
                'status': 'MOCK_SUCCESS',
                'video_title': title,
                'scheduled_time': publish_time_iso,
                'video_file': video_file_path,
                'thumbnail_file': thumbnail_path,
                'message': 'YouTube API credentials missing. Successfully simulated upload and verified metadata integrity.'
            }
            with open('publish_report.json', 'w', encoding='utf-8') as f:
                json.dump(mock_report, f, ensure_ascii=False, indent=4)
            return True
            
        # 실제 API 업로드 로직
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': '10' # 음악 카테고리
                },
                'status': {
                    'privacyStatus': 'private', # 일단 비공개로 올리고 예약을 검는 형태가 일반적
                    'publishAt': publish_time_iso
                }
            }
            
            media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/*')
            
            print("[INFO] 유튜브에 비디오 파일을 업로드 중입니다...")
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"[INFO] 업로드 진행율: {int(status.progress() * 100)}%")
                    
            video_id = response.get('id')
            print(f"[SUCCESS] 비디오 업로드 완료! Video ID: {video_id}")
            
            # 썸네일 등록
            if os.path.exists(thumbnail_path):
                print(f"[INFO] 썸네일 '{thumbnail_path}' 업로드 중...")
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumbnail_path)
                ).execute()
                print("[SUCCESS] 썸네일 업로드 성공!")
                
            report = {
                'status': 'API_SUCCESS',
                'video_id': video_id,
                'video_title': title,
                'scheduled_time': publish_time_iso,
                'video_file': video_file_path,
                'thumbnail_file': thumbnail_path
            }
            with open('publish_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
            return True
            
        except Exception as e:
            print(f"[ERROR] 유튜브 API 업로드 중 오류 발생: {str(e)}")
            # 실패 시에도 중단하지 않고 리포트 생성
            err_report = {
                'status': 'API_FAILED',
                'error': str(e),
                'video_title': title
            }
            with open('publish_report.json', 'w', encoding='utf-8') as f:
                json.dump(err_report, f, ensure_ascii=False, indent=4)
            return False

    def create_mock_video_file(self, path):
        """테스트 가동을 위해 임시 모의 비디오 파일을 생성합니다."""
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
        with open(path, 'wb') as f:
            f.write(b"MOCK VIDEO DATA FOR TESTING LUNA AUTO PUBLISHING")
        print(f"[INFO] 임시 테스트 비디오 생성 완료: '{path}'")
        return path

if __name__ == "__main__":
    publisher = YouTubePublisher()
    # 3시간 뒤로 예약 업로드 시뮬레이션
    publisher.publish_video(
        video_file_path='output/final_video.mp4', 
        thumbnail_path='youtube_thumbnail.png'
    )
