<div align="center">

<img src="assets/logo.svg" width="120" height="120" alt="StockLens logo">

# StockLens

**AI가 진짜 데이터로 분석합니다**

[![PyPI](https://img.shields.io/pypi/v/stocklens-mcp.svg)](https://pypi.org/project/stocklens-mcp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🇰🇷 **한국어** | [🇺🇸 English](README.en.md)

</div>

---

## 왜 필요한가

AI에게 차트 이미지를 보여주면 **숫자를 추측해서 틀린 분석**을 합니다 (할루시네이션).

**StockLens**는 Claude에 네이버 증권의 **실제 시세 데이터**를 직접 연결해서, AI가 추측이 아닌 **진짜 숫자를 읽고 분석**하도록 만듭니다.

```
❌ "삼성전자 8만원대인 것 같아요" (추측, 틀림)
✅ "삼성전자 206,000원, 20일 이평선 대비 +5.3%" (실제 데이터)
```

## 주요 기능

- 📊 **19개 도구** — 현재가, 차트, 수급, 재무, 스크리닝, Excel 출력
- 🔑 **API 키 불필요** — 네이버 증권 공개 데이터
- 🚀 **빠른 응답** — TTL 캐시 + Semaphore 최적화
- 📁 **Excel 스냅샷** — 한 번 스캔 → 반복 쿼리 즉시
- 🤖 **Gemini/GPT 연동** — Excel 내보내기로 다른 AI에서도 활용

## 빠른 시작

### ⭐ 방법 A: 명령어 복붙 (가장 권장)

터미널(PowerShell / cmd / Terminal) 열고 두 줄 복붙:

```bash
pip install stocklens-mcp
stocklens-setup
```

### 방법 B: 파일 다운로드 (비개발자)

[install.bat](https://github.com/Johnhyeon/stocklens-mcp/releases/latest/download/install.bat) (Windows) 또는 [install.sh](https://github.com/Johnhyeon/stocklens-mcp/releases/latest/download/install.sh) (Mac/Linux) 다운로드 → 더블클릭 실행

> ⚠️ Windows에서 파일이 **메모장으로 열리면** `install.bat.txt`로 저장된 경우. 우클릭 → "연결 프로그램" → "Windows 명령 프로세서" 선택하거나, [상세 가이드](guides/ko/INSTALL.md#step-3-stocklens-설치) 참조.

**Claude Desktop**을 완전히 종료했다가 재시작하세요.

## 동작 확인

Claude에서:
```
삼성전자 현재가 알려줘
```

종목명, 현재가, 전일대비, 거래량이 나오면 설치 완료입니다.

## 설치 문제 진단

MCP가 Claude Desktop에 안 잡히면:

```bash
stocklens-doctor
```

Python·패키지·명령·config 4단계 자동 점검. 문제 원인과 고치는 명령어까지 표시. 친구분이 막혔을 때 이 한 줄만 보내주세요.

## 사용 예시

```
"SK하이닉스 120일 일봉 보고 20일 이동평균선 기준으로 추세 판단해줘"
"카카오 외국인/기관 최근 20일 수급 분석해줘"
"시가총액 상위 100개 중 PER 15 이하인 종목 찾아줘"
"오늘 강세 테마 3개 알려주고 각 테마 주도주 분석해줘"
```

## 더 알아보기

- [📘 **도구 19개 상세** →](guides/ko/TOOLS.md)
- [💡 **프롬프트 예시 50개** →](guides/ko/USAGE.md)
- [🔧 **설치/트러블슈팅** →](guides/ko/INSTALL.md)

## 지원 환경

| 환경 | 지원 |
|------|------|
| Claude Desktop (앱) | ✅ 메인 |
| Claude Code (CLI) | ✅ |
| Claude.ai (웹) | ❌ 로컬 MCP 미지원 |
| ChatGPT / Gemini | Excel 내보내기로 우회 가능 |

## 기여

이슈, PR 모두 환영합니다. 버그 제보나 기능 요청은 [Issues](https://github.com/Johnhyeon/stocklens-mcp/issues)에 남겨주세요.

## 라이선스

MIT License
