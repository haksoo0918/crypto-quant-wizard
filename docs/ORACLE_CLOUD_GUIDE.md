# 🏛️ 오라클 클라우드(OCI) Always Free 24시간 무인 배포 가이드

본 문서는 오라클 클라우드(OCI) Always Free 티어를 이용해 **평생 무료 Linux VM + 영구 고정 공인 IP** 를 할당받고, 거래소 IP 등록 후 `crypto-quant-wizard`를 365일 무인 구동하는 공식 매뉴얼입니다.

---

## 📌 핵심 원칙 (실패 방지)
* **인스턴스 모델**: 반드시 **`VM.Standard.E2.1.Micro` (AMD)** 를 선택합니다. (ARM Ampere A1은 리전 품귀 에러가 잦으므로 피해야 합니다.)
* **IP 유형**: 인스턴스 생성 직후 기본 VNIC의 **[IP 관리]** 탭에서 **'예약된 퍼블릭 IP(Reserved Public IP)'** 로 발급/연결해야 평생 고정됩니다.

---

## 💡 핵심 용어 1분 정리
* **인스턴스 (Instance / VM)**: 오라클 데이터센터에 있는 **'24시간 켜진 가상 컴퓨터 본체'** 입니다. 내 PC를 꺼도 이 가상 컴퓨터는 계속 켜져 있습니다.
* **예약된 퍼블릭 IP (Reserved Public IP)**: 서버를 껐다 켜도 절대 바뀌지 않는 **'평생 고정 공인 IP'** 입니다. 업비트/빗썸/바이낸스에 등록해두면 이 주소에서 오는 주문만 안전하게 통과시켜 줍니다.
* **SSH 키 (`.key` 파일)**: 비밀번호 대신 쓰는 **'디지털 열쇠'** 입니다. 이 열쇠 파일이 있어야만 서버 터미널에 로그인할 수 있습니다.

---

## 1단계. 인스턴스(VM) 생성
1. **오라클 클라우드 콘솔** 로그인 (리전: 춘천, 서울, 도쿄 등)
2. 메인 화면 **[VM 인스턴스 생성]** 클릭
3. **이름**: `crypto-quant-wizard-vm`
4. **이미지 및 구성 (Image and Shape)**:
   * 이미지: **Canonical Ubuntu 24.04**
   * 구성(Shape): **`VM.Standard.E2.1.Micro`** (Always Free 적격)
5. **네트워킹**:
   * 새 가상 클라우드 네트워크(VCN) 및 공용 서브넷 자동 생성
6. **SSH 키 추가**:
   * **`자동으로 키 쌍 생성`** 선택 ➔ **`[프라이빗 키 다운로드]`** 클릭하여 PC에 안전하게 보관 (예: `~/.ssh/oci-quant.key`)
7. 하단 **`[생성]`** 클릭 ➔ 상태가 녹색 **[실행 중]** 으로 변경되는지 확인.

---

## 2단계. 평생 고정 IP(예약된 공용 IP) 할당
1. 인스턴스 상세 화면 상단 탭에서 **`[네트워킹]`** 클릭
2. 기본 VNIC 이름 클릭 ➔ 좌측/상단 메뉴 중 **`[IP 관리]`** 클릭
3. 프라이빗 IP 행 우측 **점 3개(`...`)** 클릭 ➔ **`[편집]`**
4. 모달 창 입력:
   * 퍼블릭 IP 유형: **`예약된 퍼블릭 IP`** 선택
   * 라디오 버튼: **`새 예약된 IP 생성`** 선택
   * 퍼블릭 IP 이름: `quant-bot-ip`
   * IP 주소 소스: **`Oracle`** 선택
5. 하단 **`[업데이트]`** 클릭 ➔ 발급된 영구 고정 공인 IP 확인: **`<내_고정_IP>`**

---

## 3단계. 방화벽 포트 8080 개방 (웹 대시보드 접속용)
1. OCI 콘솔 ➔ [네트워킹] ➔ [가상 클라우드 네트워크(VCN)] 클릭
2. 생성된 VCN 클릭 ➔ [보안 목록(Security Lists)] ➔ `Default Security List` 클릭
3. **[수신 규칙 추가(Add Ingress Rules)]** 클릭:
   * 소스 CIDR: `0.0.0.0/0`
   * 대상 포트 범위: `8080`
   * 설명: `Crypto Quant Wizard Web UI`
4. [수신 규칙 추가] 클릭 완료.

---

## 4단계. 거래소(업비트/빗썸/바이낸스) 고정 IP 등록
* 각 거래소 API 관리 페이지로 이동하여 **허용 IP 주소란에 `<내_고정_IP>`를 등록** 합니다:
  * **업비트**: [고객센터] ➔ [Open API 관리] ➔ IP 등록
  * **빗썸**: [고객센터] ➔ [API 관리] ➔ IP 등록
  * **바이낸스**: [API Management] ➔ [Restrict access to trusted IPs only] ➔ IP 등록

---

## 5단계. 서버 접속 및 봇 설치
1. PC 터미널에서 SSH 키를 이용하여 접속:
   ```bash
   chmod 600 ~/.ssh/oci-quant.key
   ssh -i ~/.ssh/oci-quant.key ubuntu@<내_고정_IP>
   ```
2. **시스템 업데이트 및 스왑 메모리(1GB) 생성**:
   ```bash
   sudo fallocate -l 1G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
   sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
   ```
3. **리포지토리 클론 및 실행**:
   ```bash
   git clone https://github.com/<내_계정>/crypto-quant-wizard.git
   cd crypto-quant-wizard
   chmod +x start.sh
   ```

---

## 6단계. 백그라운드 무인 24시간 구동
서버에서 아래 명령어를 실행하면 웹 서버와 백그라운드 스케줄러가 24시간 365일 무인 가동됩니다:
```bash
nohup ./start.sh > server.log 2>&1 &
```

* **웹 대시보드 및 설정 마법사 접속**:
  * PC/모바일 브라우저 주소창에 `http://<내_고정_IP>:8080` 입력.
  * 브라우저에서 거래소 API Key를 입력하고 연결 테스트 후 설정을 저장하면 끝!
* **로그 실시간 확인**:
  ```bash
  tail -f server.log
  ```
* 이제 로컬 PC를 꺼도 오라클 클라우드 VM에서 매일 09:05 KST 정기 퀀트 매매와 디스코드 리포트가 무중단으로 동작합니다.
