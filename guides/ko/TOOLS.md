# StockLens 도구 레퍼런스

총 19개 도구. 카테고리별로 정리했습니다.

[🇺🇸 English](../en/TOOLS.md) | [USAGE](USAGE.md) | [INSTALL](INSTALL.md)

---

## 📊 기본 조회 (6개)

### `search`
종목명이나 코드로 검색합니다.

**Parameters**
- `query` (str): 종목명 또는 코드

**Example**
```
"삼성전자 종목코드 알려줘"
"오이솔루션 검색"
```

---

### `get_chart`
일봉/주봉/월봉 OHLCV 데이터를 조회합니다.

**Parameters**
- `code` (str): 종목코드 6자리
- `timeframe` (str): `"day"` / `"week"` / `"month"` (기본 `"day"`)
- `count` (int): 봉 개수 (기본 120, 최대 500)

**Example**
```
"삼성전자 120일 일봉 보여줘"
"SK하이닉스 주봉 60개 가져와"
```

---

### `get_price`
실시간 현재가 + 시가/고가/저가/거래량.

**Parameters**
- `code` (str): 종목코드 6자리

**Example**
```
"삼성전자 지금 얼마야?"
"현대차 현재가"
```

---

### `get_flow`
투자자별 매매동향 (외국인/기관 순매매).

**Parameters**
- `code` (str): 종목코드 6자리
- `days` (int): 조회 일수 (기본 20, 최대 60)

**Example**
```
"카카오 20일 외국인 수급 분석해줘"
"SK하이닉스 최근 한 달 기관 매매 동향"
```

**참고**: 네이버 증권은 개인 순매매 컬럼을 제공하지 않아 반환하지 않습니다.

---

### `get_financial`
재무지표 (PER, PBR, 시가총액, EPS, BPS 등).

**Parameters**
- `code` (str): 종목코드 6자리

**Example**
```
"네이버 PER이랑 PBR 알려줘"
"현대차 재무지표"
```

---

### `get_index`
KOSPI / KOSDAQ 지수 현재값.

**Parameters**
- 없음

**Example**
```
"오늘 코스피 어때?"
"시장 지수 보여줘"
```

---

## 🔍 스크리닝 (7개)

### `list_themes`
네이버 증권 테마 목록 (등락률 순).

**Parameters**
- `page` (int): 페이지 (기본 1, 최대 7)

**Example**
```
"오늘 강세 테마 10개 보여줘"
"테마 목록 2페이지"
```

테마는 한 페이지당 40개, 총 7페이지 (약 280개 테마).

---

### `get_theme_stocks`
특정 테마에 속한 종목 리스트.

**Parameters**
- `theme_name` (str): 테마명 (부분 매칭 지원)
- `count` (int): 최대 반환 개수 (기본 30, 최대 50)
- `include_reason` (bool): 편입사유 포함 여부 (기본 `true`, `false`면 토큰 절감)

**Example**
```
"AI 반도체 테마 종목"
"2차전지 관련주 20개만"
```

---

### `list_sectors`
업종(섹터) 목록 (약 79개, 등락률 순).

**Parameters**
- 없음

**Example**
```
"업종별 현황 보여줘"
"섹터 리스트"
```

---

### `get_sector_stocks`
특정 업종에 속한 종목 리스트.

**Parameters**
- `sector_name` (str): 업종명 (부분 매칭)
- `count` (int): 최대 반환 개수 (기본 30, 최대 50)

**Example**
```
"통신장비 업종 종목"
"반도체 섹터 30개"
```

---

### `get_volume_ranking`
거래량 상위 종목.

**Parameters**
- `market` (str): `"KOSPI"` / `"KOSDAQ"` / `"ALL"` (기본 `"ALL"`)
- `count` (int): 개수 (기본 50, 최대 500)

**Example**
```
"오늘 거래량 상위 50개"
"코스피 거래량 TOP 100"
```

---

### `get_change_ranking`
등락률 상위/하위 종목.

**Parameters**
- `direction` (str): `"up"` (상승) / `"down"` (하락), 기본 `"up"`
- `market` (str): `"KOSPI"` / `"KOSDAQ"` / `"ALL"` (기본 `"ALL"`)
- `count` (int): 개수 (기본 50, 최대 500)

**Example**
```
"오늘 상한가 종목들"
"코스닥 하락률 상위 20개"
```

---

### `get_market_cap_ranking`
시가총액 상위 종목.

**Parameters**
- `market` (str): `"KOSPI"` / `"KOSDAQ"` (기본 `"KOSPI"`)
- `count` (int): 개수 (기본 50, 최대 500)

**Example**
```
"시가총액 상위 100개"
"코스닥 시총 50위까지"
```

---

## ⚡ 벌크 조회 (2개)

### `get_multi_stocks`
여러 종목의 기본 정보(현재가/거래량)를 한 번에 병렬 조회.

**Parameters**
- `codes` (list[str]): 종목코드 리스트 (최대 30개)

**Example**
```
"삼성전자, SK하이닉스, 현대차 한번에 보여줘"
```

**왜 씀**: N개 종목을 개별 `get_price`로 호출하는 것보다 훨씬 빠름.

---

### `get_multi_chart_stats`
여러 종목의 차트 통계 (52주 고점/저점/낙폭) 병렬 조회.

**Parameters**
- `codes` (list[str]): 종목코드 리스트 (최대 100개)
- `days` (int): 기간 (기본 260 = 52주)

**Example**
```
"시총 100개의 52주 낙폭 보여줘"
```

**반환 필드**: `current_price`, `high`, `high_date`, `low`, `low_date`, `drawdown_pct`, `recovery_pct`, `period_return_pct`, `avg_volume`

---

## 📁 Excel 출력 (3개)

### `export_to_excel`
단일 종목 데이터를 Excel 파일로 저장.

**Parameters**
- `data_type` (str): `"chart"` / `"flow"` / `"financial"`
- `code` (str): 종목코드 6자리
- `days` (int): chart/flow 기간 (기본 180)
- `filename` (str): 파일명 (비우면 자동 생성)

**Example**
```
"삼성전자 차트 데이터 엑셀로 저장해줘"
"현대차 수급 엑셀 파일로"
```

**용도**: Gemini/GPT 등 다른 AI에 파일 업로드로 넘길 때.

---

### `scan_to_excel`
여러 종목을 스캔해서 Excel 스냅샷 생성.

**Parameters**
- `codes` (list[str]): 종목코드 리스트 (최대 500개)
- `days` (int): 차트 통계 기간 (기본 260)
- `include_financial` (bool): 재무지표 포함 (기본 `true`)
- `filename` (str): 파일명 (비우면 자동)

**Example**
```
"시총 상위 100개로 스냅샷 만들어줘"
```

**워크플로우**: 한 번 스캔(10~20초) → 이후 `query_excel`로 즉시 반복 쿼리 (16ms).

---

### `query_excel`
저장된 Excel 스냅샷에서 조건 필터링.

**Parameters**
- `file_path` (str): `scan_to_excel`로 만든 파일 경로
- `filters` (dict): 필터 조건 (예: `{"per_max": 10, "drawdown_pct_max": -30}`)
- `sort_by` (str): 정렬 컬럼
- `descending` (bool): 내림차순 (기본 `true`)
- `limit` (int): 상위 N개 (기본 30)

**Example**
```
"그 스냅샷에서 PER 10 이하 찾아줘"
"낙폭 -20% 이상인 종목만"
```

---

## 🔧 디버깅 (1개)

### `get_metrics_summary`
최근 N일간 도구 사용량 통계.

**Parameters**
- `days` (int): 조회 일수 (기본 1, 최대 30)

**Example**
```
"오늘 도구 사용 통계"
"최근 일주일 토큰 소모량"
```

**로그 위치**: `~/Downloads/kstock/logs/metrics_YYYYMMDD.jsonl`

---

## 저장 파일 위치

Excel 스냅샷, 차트 파일, 메트릭 로그는 모두:

- Windows: `%USERPROFILE%\Downloads\kstock\`
- macOS/Linux: `~/Downloads/kstock/`

사용자 PC에만 저장되며, 외부로 전송되지 않습니다.
