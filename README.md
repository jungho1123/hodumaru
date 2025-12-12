# Compliance-First AI SNS Agent (Windows Edition) v3.1

## 1. 개요 및 목적 (Overview & Purpose)
**Compliance-First AI SNS Agent**는 Meta(Facebook/Instagram)의 엄격한 정책을 100% 준수하며, Windows 로컬 환경에서 안전하게 구동되는 자동화 파이프라인입니다.
"Human-in-the-loop" 철학에 따라 AI가 생성한 콘텐츠를 사용자가 최종 승인해야만 게시되며, 개인정보 보호를 위한 자동 데이터 파기(Data Deletion) 시스템이 내장되어 있습니다.

## 2. 기술 스택 (Tech Stack)
*   **OS**: Windows 10/11 (WSL2 Architecture)
*   **Core**: Docker Desktop (running on WSL2 Backend)
*   **Control Tower**: n8n (Self-hosted via Docker)
*   **Database**: PostgreSQL 16 (Local Container)
*   **Infrastructure**: AWS S3 (Private Bucket + Lifecycle Rules), AWS Lambda (Serverless Functions)
*   **Auth & Compliance**: Python Flask (Local OAuth Server), ngrok (Tunneling)

## 3. 설치 방법 (Installation)
### 필수 요구 사항
*   Windows 10/11 (WSL2 활성화 필수)
*   Docker Desktop 설치 및 실행
*   Python 3.9+

### 단계별 설치
1.  **레포지토리 클론**
    ```bash
    git clone https://github.com/your-repo/compliance-ai-agent.git
    cd compliance-ai-agent
    ```
2.  **파이썬 의존성 설치 (Auth Server & Lambda)**
    ```bash
    pip install -r auth_server/requirements.txt
    pip install -r lambda/requirements.txt
    ```
3.  **인프라 디렉토리 생성 (최초 1회)**
    ```bash
    mkdir n8n_data
    ```

## 4. 실행 방법 (Execution)
1.  **Docker 서비스 시작 (n8n + DB)**
    ```bash
    docker compose up -d
    ```
2.  **로컬 Auth Server 실행** (OAuth, Privacy Policy, Deletion Callback 제공)
    ```bash
    python auth_server/app.py
    ```
3.  **ngrok 터널링 시작** (외부에서 내 로컬 서버 접속 허용)
    ```bash
    ngrok http 5000
    ```
4.  **n8n 설정**
    *   브라우저에서 [http://localhost:5678](http://localhost:5678) 접속
    *   `n8n_workflows/` 폴더의 JSON 파일 Import
    *   PostgreSQL 및 Google/OpenAI Credentials 설정

## 5. 제공 기능 (Key Features)
*   **Secure Drafting**: Google Photos 사진을 S3(Private)에 업로드하고, AI가 안전한 캡션을 생성하여 DB에 임시 저장.
*   **Authorized Publishing**: 사용자가 승인한 콘텐츠만 인스타그램에 게시.
*   **Compliance Ready**: Meta 앱 검수 통과를 위한 데이터 삭제 콜백(Data Deletion Callback) 및 개인정보처리방침 페이지 내장.

## 6. Github 링크
*   [Repository URL Placeholder]
