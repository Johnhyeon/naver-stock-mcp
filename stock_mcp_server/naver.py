"""네이버 증권에서 주식 데이터를 수집하는 모듈."""

import httpx
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import json
import re


BASE_URL = "https://finance.naver.com"
FCHART_URL = "https://fchart.stock.naver.com/siseJson.nhn"
TIMEOUT = 10.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def _parse_int(text: str, default: int = 0) -> int:
    """'+1,234', '-1,234', '1,234', '-' 등을 정수로 변환합니다."""
    if text is None:
        return default
    cleaned = text.strip().replace(",", "").replace("+", "")
    if not cleaned or cleaned == "-":
        return default
    try:
        return int(cleaned)
    except ValueError:
        return default


async def search_stock(query: str) -> list[dict]:
    """종목명 또는 코드로 검색하여 종목 코드를 반환합니다."""
    # 메인 사이트 검색 페이지 사용 (ac.finance.naver.com보다 안정적)
    url = f"{BASE_URL}/search/searchList.naver"
    params = {"query": query}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(url, params=params, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "lxml")

    results = []
    # 검색 결과 테이블에서 종목명+코드 추출
    links = soup.select("a.tit")
    for link in links:
        href = link.get("href", "")
        name = link.text.strip()
        # /item/main.naver?code=005930 형태에서 코드 추출
        code_match = re.search(r"code=(\d{6})", href)
        if code_match and name:
            results.append({
                "code": code_match.group(1),
                "name": name,
            })
    return results[:5]


async def get_ohlcv(
    code: str,
    timeframe: str = "day",
    count: int = 60,
) -> list[dict]:
    """네이버 차트 API에서 OHLCV(시가/고가/저가/종가/거래량) 데이터를 가져옵니다.

    Args:
        code: 종목코드 (예: "005930")
        timeframe: "day"(일봉), "week"(주봉), "month"(월봉)
        count: 가져올 봉 개수 (기본 60개)
    """
    params = {
        "symbol": code,
        "timeframe": timeframe,
        "count": count,
        "requestType": "0",
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(FCHART_URL, params=params, headers=HEADERS)
        text = resp.text

    # 네이버 fchart 응답은 JS 배열 형태 → 파싱
    text = text.strip()
    rows = []
    for line in text.split("\n"):
        line = line.strip().strip(",")
        if not line or line.startswith("[") and "날짜" in line:
            continue
        if line == "]":
            continue
        # ['20250401', 67800, 68200, 67100, 67500, 12345678]
        line = line.strip("[]")
        parts = [p.strip().strip("'\"") for p in line.split(",")]
        if len(parts) >= 6:
            try:
                rows.append({
                    "date": parts[0].strip(),
                    "open": int(parts[1]),
                    "high": int(parts[2]),
                    "low": int(parts[3]),
                    "close": int(parts[4]),
                    "volume": int(parts[5]),
                })
            except (ValueError, IndexError):
                continue

    return rows


async def get_current_price(code: str) -> dict:
    """종목의 현재가 정보를 가져옵니다."""
    url = f"{BASE_URL}/item/main.naver?code={code}"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "lxml")

    result = {"code": code}

    # 종목명
    name_tag = soup.select_one("div.wrap_company h2 a")
    if name_tag:
        result["name"] = name_tag.text.strip()

    # 현재가
    price_tag = soup.select_one("p.no_today span.blind")
    if price_tag:
        result["price"] = int(price_tag.text.replace(",", ""))

    # 전일대비
    diff_tag = soup.select_one("p.no_exday em span.blind")
    if diff_tag:
        diff_text = diff_tag.text.replace(",", "")
        # 상승/하락 판단
        icon = soup.select_one("p.no_exday em.no_up, p.no_exday em.no_down")
        if icon and "no_down" in icon.get("class", []):
            diff_text = "-" + diff_text
        result["change"] = int(diff_text)

    # 거래량
    table = soup.select("table.no_info tr")
    for tr in table:
        th = tr.select_one("th")
        td = tr.select_one("td span.blind")
        if th and td:
            label = th.text.strip()
            value = td.text.replace(",", "").strip()
            if "거래량" in label:
                result["volume"] = int(value)
            elif "시가" in label:
                result["open"] = int(value)
            elif "고가" in label:
                result["high"] = int(value)
            elif "저가" in label:
                result["low"] = int(value)

    return result


async def get_investor_flow(code: str, days: int = 20) -> list[dict]:
    """투자자별 매매동향 (기관/외국인 순매매)을 가져옵니다.

    네이버 증권 frgn.naver 페이지 기준:
    - 두 번째 table.type2가 수급 데이터 테이블
    - 컬럼 순서: 날짜 | 종가 | 전일비 | 등락률 | 거래량 | 기관 순매매 | 외국인 순매매 | 보유주수 | 지분율
    - 개인 순매매 컬럼은 이 페이지에 없음
    """
    url = f"{BASE_URL}/item/frgn.naver"
    results = []
    page = 1

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        while len(results) < days:
            params = {"code": code, "page": page}
            resp = await client.get(url, params=params, headers=HEADERS)
            soup = BeautifulSoup(resp.text, "lxml")

            # 두 번째 table.type2가 수급 데이터 (첫 번째는 거래원)
            tables = soup.select("table.type2")
            if len(tables) < 2:
                break

            table = tables[1]
            rows = table.select("tr")
            found_in_page = 0
            for row in rows:
                cols = row.select("td")
                # 수급 데이터 행은 정확히 9개 td를 가짐
                if len(cols) != 9:
                    continue

                date_text = cols[0].text.strip()
                # 날짜 형식(YYYY.MM.DD) 체크 — 헤더/빈 행 필터링
                if not date_text or "." not in date_text:
                    continue

                try:
                    result = {
                        "date": date_text,
                        "close": _parse_int(cols[1].text),
                        "change": _parse_int(cols[2].text.split()[-1] if cols[2].text.strip() else "0"),
                        "volume": _parse_int(cols[4].text),
                        "institutional": _parse_int(cols[5].text),
                        "foreign": _parse_int(cols[6].text),
                    }
                    results.append(result)
                    found_in_page += 1
                except (ValueError, IndexError):
                    continue

            if found_in_page == 0:
                break  # 더 이상 데이터 없음

            if len(results) >= days:
                break
            page += 1
            if page > 10:
                break

    return results[:days]


async def get_financials(code: str) -> dict:
    """종목의 주요 재무지표를 가져옵니다."""
    url = f"{BASE_URL}/item/main.naver?code={code}"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "lxml")

    result = {"code": code}

    # 종목명
    name_tag = soup.select_one("div.wrap_company h2 a")
    if name_tag:
        result["name"] = name_tag.text.strip()

    # 투자정보 테이블 (PER, PBR, 배당수익률 등)
    cop_info = soup.select("div.cop_analysis table")
    if cop_info:
        for table in cop_info:
            headers = [th.text.strip() for th in table.select("th")]
            rows = table.select("tr")
            for row in rows:
                th = row.select_one("th")
                tds = row.select("td")
                if th and tds:
                    label = th.text.strip()
                    values = [td.text.strip() for td in tds]
                    if values:
                        result[label] = values

    # 시가총액, 상장주식수 등
    aside = soup.select("div.first table tr")
    for tr in aside:
        th = tr.select_one("th")
        td = tr.select_one("td")
        if th and td:
            label = th.text.strip()
            value = td.text.strip()
            if "시가총액" in label or "상장주식수" in label or "PER" in label or "PBR" in label:
                result[label] = value

    return result


async def get_market_index() -> list[dict]:
    """KOSPI, KOSDAQ 지수 현재값을 가져옵니다."""
    url = f"{BASE_URL}/sise/sise_index.naver?code=KOSPI"
    url2 = f"{BASE_URL}/sise/sise_index.naver?code=KOSDAQ"

    results = []
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for idx_url, name in [(url, "KOSPI"), (url2, "KOSDAQ")]:
            resp = await client.get(idx_url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, "lxml")

            now_val = soup.select_one("div#now_value")
            change_val = soup.select_one("div#change_value_and_rate")

            item = {"index": name}
            if now_val:
                item["value"] = now_val.text.strip().replace(",", "")
            if change_val:
                item["change"] = change_val.text.strip()
            results.append(item)

    return results
