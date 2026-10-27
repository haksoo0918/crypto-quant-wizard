# 베이스 이미지: 경량 Python 3.11 Slim
FROM python:3.11-slim

# 환경 변수 설정 (버퍼링 방지 및 타임존 KST)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Seoul

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 필수 유틸리티 및 타임존 데이터 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    curl \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# 패키지 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 복사
COPY src/ ./src/
COPY docs/ ./docs/

# 데이터 및 로그 저장 디렉토리 생성
RUN mkdir -p data logs

# 웹 서비스 포트 노출
EXPOSE 8080

# 헬스체크
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/api/status || exit 1

# 서버 실행 (FastAPI + 내장 APScheduler)
CMD ["python", "src/server.py"]
