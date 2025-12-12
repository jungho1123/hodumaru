# Project Context & Architecture

## 1. 핵심 파일 구조 (Core File Structure)
```
/ (Project Root)
├── auth_server/             # Local Flask Server for Compliance
│   ├── app.py               # OAuth2 & Deletion Callback Logic
│   └── templates/           # HTML Pages (Login, Privacy, TOS)
├── database/                # Database Setup
│   └── schema.sql           # Tables: users, drafts, performance_log
├── infrastructure/          # IaC & Scripts
│   └── aws-setup.sh         # S3 Setup Script
├── lambda/                  # AWS Lambda Functions
│   ├── data_deletion.py     # Meta Deletion Callback Handler
│   └── image_processor.py   # S3 Upload & Presigning
├── n8n_workflows/           # Automation Pipelines
│   ├── secure_drafting.json # Photo -> Draft Flow
│   └── authorized_publishing.json # Draft -> Instagram Flow
├── docker-compose.yml       # Local n8n + Postgres stack
└── template.yaml            # AWS SAM Deployment Template
```

## 2. 데이터 명세 (Data Specifications)
### Database: PostgreSQL
*   **`users`**: Meta 유저 정보 및 Access Token 저장 (암호화 필요).
*   **`drafts`**: AI가 생성한 게시물 초안.
    *   `status`: `PENDING` (대기) -> `APPROVED` (승인) -> `PUBLISHED` (게시됨).
    *   `image_url`: S3 Presigned URL (보안상 유효기간 존재).
*   **`performance_log`**: 개인정보가 제거된 로깅 데이터.

### Storage: AWS S3
*   **Lifecycle Rule**: 업로드된 이미지는 48시간 후 자동 영구 삭제 (개인정보 보호 정책).
*   **Access**: `Private` 권한이 기본이며 Presigned URL을 통해서만 제한적 접근.

## 3. 기술적 제약 사항 (Technical Constraints)
1.  **Windows Environment**:
    *   Lambda 함수(특히 Python C-extension 사용 시)는 반드시 WSL2 리눅스 환경에서 빌드/배포해야 함.
    *   Docker Desktop은 Hyper-V/WSL2 백엔드가 활성화되어 있어야 함.
2.  **Meta Webhook Testing**:
    *   로컬 개발 시 `localhost`는 Meta 서버에서 접근 불가하므로 반드시 `ngrok` 등을 사용해 HTTPS 터널링을 해야 함.
    *   ngrok 주소가 바뀔 때마다 Meta App Dashboard에서 URL 업데이트 필요 (무료 버전 한계).
3.  **Token Expiry**:
    *   Facebook User Access Token은 일정 시간(보통 60일) 후 만료되므로 갱신 메커니즘 필요.

## 4. 개선 사항 (Improvements / Roadmap)
*   **Auth Server Cloud Deployment**: 로컬 Flask 서버를 AWS Lambda + API Gateway로 이전하여 상시 가동 상태 유지.
*   **Auto-Ngrok**: 실행 시 자동으로 ngrok URL을 가져와 환경변수에 주입하는 스크립트 작성.
*   **Secret Management**: `docker-compose.yml` 및 코드 내 하드코딩된 비밀 키를 `.env` 파일 또는 Docker Secrets로 분리.
