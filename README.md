# 🧙 Crypto Quant Wizard

> [!WARNING]
> **🚨 현재 개발 및 내부 테스트 진행 중인 프로젝트입니다.**
> 본 프로젝트는 현재 기능 개발 및 테스트가 진행 중인 상태로 아직 최종 마무리가 되지 않았습니다. 예기치 않은 오류가 발생할 수 있으므로 개발 및 안정성 검증이 완료될 때까지 실제 사용을 자제해 주시기 바랍니다.

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![Supported Exchanges](https://img.shields.io/badge/Exchanges-Upbit%20%7C%20Bithumb%20%7C%20Binance-orange)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**누구나 5분 만에 시작하는 3대 거래소 암호화폐 퀀트 자동매매 & 웹 대시보드 마법사**

[🚀 3분 빠른 시작](#-3분-빠른-시작-quick-start) •
[🌟 핵심 기능](#-핵심-기능) •
[📊 거래소 및 전략 매핑](#-거래소-및-전략-매핑) •
[🏛️ 오라클 클라우드 24시간 무인 구동](#️-오라클-클라우드-always-free-24시간-무인-구동) •
[🛡️ 보안 원칙](#️-보안-원칙)

</div>

---

## 💡 프로젝트 소개

`Crypto Quant Wizard`는 코딩이나 복잡한 서버 설정 지식이 없는 개인 투자자도 **클론(Clone) 후 `start.bat` 또는 `start.sh` 한 번만 실행하면 웹 브라우저에서 5분 만에 설정을 끝마치고 자동매매를 가동할 수 있는 올인원 오픈소스 퀀트 트레이딩 플랫폼** 입니다.

- **Zero-Build, Zero-Friction**: Node.js나 복잡한 빌드 도구 필요 없음! Python 하나로 웹 UI와 매매 엔진이 즉시 실행됩니다.
- **거래소-전략 분리 매핑**: 사용자가 원하는 거래소(업비트, 빗썸, 바이낸스)를 선택하고, 검증된 퀀트 전략을 드롭다운으로 자유롭게 연결합니다.
- **일체형 스케줄러 (All-in-One)**: 웹 서버 프로세스 안에 **매일 09:05 KST 자동 매매 엔진** 이 내장되어 있어 별도의 복잡한 스케줄러 등록 없이 실행 즉시 정기 매매 대기 상태가 됩니다.
- **오라클 클라우드 Always Free 최적화**: 로컬 PC를 24시간 켜두지 않고 평생 무료 클라우드 VM에 올려 365일 무인 가동할 수 있습니다.

---

## 🌟 핵심 기능

| 구분 | 주요 기능 | 설명 |
| :--- | :--- | :--- |
| 🧙 **설정 마법사 (Wizard)** | 원클릭 웹 온보딩 | 첫 실행 시 브라우저에서 거래소 API Key 입력 및 **[연결 테스트]** 로 즉시 검증 |
| 🔀 **전략 분리 매핑** | Decoupled Architecture | 각 거래소별로 적용할 퀀트 전략(50:50 동적 리밸런싱, SuperTrend 추세추종 등)을 개별 선택 |
| 📊 **범용 웹 대시보드** | 모던 핀테크 UI | 당일 신호등 지침, Chart.js 60일 기술 지표 시계열 차트, 자산 성장 곡선, 실거래 체결 장부 |
| ⏰ **일체형 스케줄러** | 백그라운드 자동화 | 매일 오전 09:05 KST(일봉 마감 직후) 정기 매매 분석/주문 집행 및 디스코드 리포트 전송 |
| ⚡ **즉시 실행 (Run Now)** | 수동 1회 트리거 | 대시보드에서 버튼 클릭 한 번으로 지금 즉시 분석 및 매매 1회 실행 |
| 📜 **실시간 로그 뷰어** | 터미널 콘솔 스트리밍 | 웹 화면에서 봇의 실시간 실행 로그와 체결 내역을 3초마다 자동 확인 |

---

## 🚀 3분 빠른 시작 (Quick Start)

### 1. 리포지토리 클론 (Clone)
```bash
git clone https://github.com/<내_계정>/crypto-quant-wizard.git
cd crypto-quant-wizard
```

### 2. 원클릭 실행

#### 🖥️ Windows 사용자
폴더 안의 **`start.bat`** 파일을 더블 클릭합니다.
> 가상환경 생성, 필수 라이브러리 자동 설치, 웹 서버 기동 후 기본 브라우저(`http://localhost:8080`)가 자동으로 열립니다.

#### 🐧 Linux / macOS / Oracle Cloud 사용자
터미널에서 아래 명령어를 실행합니다:
```bash
chmod +x start.sh
./start.sh
```

#### 🐳 Docker 사용자
`ash
docker compose up -d
`
> 백그라운드로 24시간 실행되며, 브라우저에서 http://localhost:8080 (또는 서버IP:8080)으로 접속합니다.

### 3. 웹 화면에서 설정 마치기
1. 브라우저가 열리면 **[⚙️ 설정 마법사]** 탭이 나타납니다.
2. 운용 모드를 선택합니다 (`🟢 모의투자(Dry-Run)` 권장).
3. 사용할 거래소의 API Key를 입력하고 **[연결 테스트]** 버튼을 눌러 정상 연결되는지 확인합니다.
4. 거래소별로 원하는 전략을 드롭다운에서 선택합니다.
5. 디스코드 알림을 원할 경우 웹훅 URL을 입력하고 **[테스트 발송]** 을 확인합니다.
6. 하단의 **[💾 설정 저장하기]** 버튼을 클릭하면 완료! **[📊 대시보드]** 로 자동 전환됩니다.

### 4. ⏰ 상시 스케줄링 및 봇 종료 / 삭제 방법

* **스케줄러 자동 대기 (매일 실행할 필요 없음)**:
  * `start.bat` (또는 `start.sh`)을 실행하면 웹 대시보드와 함께 **내부 자동 스케줄러(APScheduler)** 가 백그라운드에서 상시 대기합니다.
  * 터미널 창을 켜두시기만 하면, 매일 아침 `09:05 KST`(일봉 마감 직후)에 봇이 자동으로 시장 데이터를 분석하고 매매 사이클을 실행합니다. (사용자가 매일 `start.bat` 을 누를 필요가 없습니다.)
* **스케줄 일시정지 및 끄기 (웹 화면에서 1초 만에 해제)**:
  * 웹 대시보드 상단 배너의 **`[⏰ 매일 09:05 KST 자동실행]`** 배지 버튼을 클릭하면 즉시 정기 스케줄이 비활성화(삭제) 상태로 전환됩니다.
  * 설정 마법사에서도 **`[스케줄 자동 실행 활성화]`** 체크를 해제하면 정기 스케줄이 중지되며, 상단 **`[⚡ 지금 1회 수동 실행]`** 버튼을 누를 때만 매매가 수행됩니다.
* **윈도우 작업 스케줄러(OS 부팅 자동실행) 등록 및 삭제**:
  * **등록**: `scripts/register_windows_task.bat` 을 더블 클릭하면 PC 부팅/로그인 시 봇이 자동 실행되도록 윈도우 스케줄러에 등록됩니다.
  * **삭제**: `scripts/unregister_windows_task.bat` 을 더블 클릭하면 등록된 윈도우 스케줄 작업이 1초 만에 완전 삭제됩니다.
  * *(수동 삭제: `Win + R` ➔ `taskschd.msc` 실행 ➔ `CryptoQuantWizard` 우클릭 후 [삭제])*
* **컴퓨터를 껐다 켰을 때**:
  * PC를 재부팅했거나 터미널을 닫았다면, 다음 날 09:05 전에 `start.bat` 을 다시 한 번만 더블 클릭해서 켜두시면 됩니다.
* **터미널 종료 방법**:
  * 터미널 창을 클릭한 뒤 **`Ctrl + C`** 를 누르고 `y`를 입력하거나, 창 우측 상단의 **`X`** (닫기) 버튼을 누르면 즉시 안전하게 종료됩니다.
* **💡 PC를 24시간 켜두기 번거로우시다면?**:
  * 집 컴퓨터를 끄고도 365일 무중단으로 돌리려면 [오라클 클라우드 Always Free 평생 무료 배포 가이드](docs/ORACLE_CLOUD_GUIDE.md)를 참고하여 무료 클라우드 VM에 올려두세요!

---

## 📊 거래소 및 전략 매핑

본 프로젝트는 수년간의 실데이터 백테스트와 실거래를 통해 검증된 3대 퀀트 모델을 제공합니다:

```
┌─────────────────────────────────────────────────────────────┐
│                       거래소 선택                           │
├───────────────┬─────────────────────────────┬───────────────┤
│ 업비트(Upbit) │        빗썸(Bithumb)        │ 바이낸스(USDT)│
└───────┬───────┴──────────────┬──────────────┴───────┬───────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ BTC/ETH 50:50 │      │ 이더리움 단독 │      │ BTC/ETH 50:50 │
│ 동적 리밸런싱 │      │ SuperTrend    │      │ 글로벌 테더   │
│ (220d SMA/ATR)│      │ (7, 3.5)+50SMA│      │ (200d SMA/ATR)│
└───────────────┘      └───────────────┘      └───────────────┘
```

1. **업비트 메인 (BTC / ETH 50:50 듀얼 모멘텀 리밸런싱)**:
   - **BTC**: 220일 SMA 대비 ±2% 노이즈 필터링 (상승 돌파 시 매수, 하향 이탈 시 매도)
   - **ETH**: 50일 SMA 대비 14일 ATR 1.5배 채널 필터링
   - **동적 리밸런싱**: 한쪽 코인이 총자산의 60%를 초과할 경우 초과분을 시장가 매도하여 현금 비중 50%를 철저히 보존.

2. **빗썸 서브 (이더리움 SuperTrend + 50일 SMA 추세 추종)**:
   - **지표**: SuperTrend(기간 7, 승수 3.5) 동적 변동성 밴드 + 50일 SMA 대추세 기준선
   - **매매**: 상승 파동 시 빗썸 자산 100% 이더리움 풀매수 집중, 하락 추세 전환 시 즉시 100% 원화 현금화 (MDD -25% 철저 방어).

3. **바이낸스 메인 (BTC / ETH 50:50 글로벌 테더 리밸런싱)**:
   - 김치프리미엄 노이즈가 없는 글로벌 테더(USDT) 마켓에서 달러 자산 증식.
   - **BTC**: 200일 SMA 대비 ±2% 버퍼 / **ETH**: 40일 SMA 대비 14일 ATR 1.2배 채널.

---

## 🏛️ 오라클 클라우드 (Always Free) 24시간 무인 구동

로컬 PC를 24시간 켜둘 필요 없이, 오라클 클라우드의 **평생 무료 Linux VM (`VM.Standard.E2.1.Micro`)** 에 올려 365일 무인 가동할 수 있습니다.

1. **서버 접속 후 클론**:
   ```bash
   git clone https://github.com/<내_계정>/crypto-quant-wizard.git
   cd crypto-quant-wizard
   chmod +x start.sh
   ```
2. **백그라운드 24시간 실행**:
   ```bash
   nohup ./start.sh > server.log 2>&1 &
   ```
3. **접속**: 브라우저 주소창에 `http://<오라클_고정_IP>:8080` 입력 후 설정 마법사에서 키 입력 및 가동.

> 📖 **자세한 OCI VM 무료 생성 및 고정 IP 발급 방법** 은 [docs/ORACLE_CLOUD_GUIDE.md](file:///c:/Users/hakso/_work/crypto-quant-wizard/docs/ORACLE_CLOUD_GUIDE.md) 매뉴얼을 참고하세요.

---

## 🛡️ 보안 원칙 (Security First)

- **절대적 로컬 보안**: 사용자가 웹 화면에서 입력한 API Key와 Secret은 오직 사용자의 로컬 머신(`.env` 및 `data/config.json`)에만 저장되며, 외부 어떤 서버로도 전송되지 않습니다.
- **Git 커밋 원천 방지**: `.gitignore`에 `.env`, `*.key`, `data/*` 및 모든 로그 파일이 등록되어 있어, 프로젝트를 GitHub에 푸시하더라도 **개인 API Key나 자산/거래 내역이 실수로 노출될 위험이 원천 차단** 됩니다.
- **자산 마스킹 보호**: 대시보드 우측 상단의 `👁️` 아이콘을 클릭하면 주변 시선(Shoulder Surfing)으로부터 자산 수치와 보유량을 즉시 블러(Blur) 처리할 수 있습니다.

---

## 📂 프로젝트 구조

```
crypto-quant-wizard/
├── start.bat                 # Windows 원클릭 런처 (가상환경 자동 설치 및 브라우저 오픈)
├── start.sh                  # Linux / Mac / Oracle Cloud 원클릭 런처
├── requirements.txt          # 패키지 의존성 (FastAPI, APScheduler, PyUpbit 등)
├── .env.example              # 환경 변수 설정 템플릿
├── .gitignore                # 시크릿 키 및 개인 거래 데이터 커밋 방지
├── PRD.md                    # 상품 요구사항 정의서
├── docs/                     # 웹 대시보드 및 마법사 프론트엔드
│   ├── index.html            # 모던 단일 페이지 SPA (마법사 + 대시보드 + 로그)
│   ├── ORACLE_CLOUD_GUIDE.md # 오라클 클라우드 Always Free 24시간 구축 매뉴얼
│   └── icons/                # 브랜드 아이콘
├── src/                      # 핵심 백엔드 및 퀀트 엔진
│   ├── server.py             # FastAPI 웹 서버 + APScheduler 일체형 백엔드
│   ├── config.py             # 거래소-전략 분리 설정 매니저
│   ├── main.py               # 3대 거래소 퀀트 통합 오케스트레이터
│   ├── indicators.py         # SMA, ATR, SuperTrend 공통 지표 엔진
│   ├── bithumb_api.py        # 빗썸 REST API 클라이언트
│   ├── binance_api.py        # 바이낸스 현물 REST API 클라이언트
│   └── discord_bot.py        # 디스코드 리포트 포맷터
└── data/                     # (로컬 보관) 거래 장부 및 자산 시계열 데이터
    ├── trade_history.csv     # 실거래 주문 체결 원장
    └── asset_history.csv     # 일자별 총자산 성장 곡선 원장
```

---

## 📜 라이선스 (License)

This project is licensed under the MIT License - see the LICENSE file for details.
