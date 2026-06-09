@echo off
echo ==========================================================
echo               MusicAI World - YouTube Automation
echo                  Powered by Agent Luna
echo ==========================================================
echo.

:: 파이썬 패키지 의존성 설치 확인
echo [System] 파이썬 의존성 패키지를 확인합니다...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [System] [Error] 의존성 패키지 설치 실패! 파이썬 설정을 확인하세요.
    pause
    exit /b %errorlevel%
)

echo.
:: 자동화 엔진 실행
echo [System] 루나 자동화 엔진을 기동합니다...
python src/main.py

echo.
echo ==========================================================
echo [System] 프로세스가 완료되었습니다.
pause
