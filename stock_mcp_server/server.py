"""한국 주식 데이터 MCP 서버.

네이버 증권에서 차트, 수급, 재무 데이터를 가져와
Claude에서 자연어로 분석할 수 있게 해줍니다.
"""

import functools
import httpx

from mcp.server.fastmcp import FastMCP
from stock_mcp_server.naver import (
    search_stock,
    get_ohlcv,
    get_current_price,
    get_investor_flow,
    get_financials,
    get_market_index,
)


def safe_tool(func):
    """MCP 도구 함수의 예외를 사용자 친화적 메시지로 변환합니다."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.TimeoutException:
            return "⚠️ 네이버 증권 응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요."
        except httpx.ConnectError:
            return "⚠️ 네이버 증권에 연결할 수 없습니다. 인터넷 연결을 확인해주세요."
        except httpx.HTTPError as e:
            return f"⚠️ 네트워크 오류가 발생했습니다: {type(e).__name__}"
        except Exception as e:
            return (
                f"⚠️ 데이터 처리 중 오류가 발생했습니다: {type(e).__name__}\n"
                f"종목코드가 올바른지, 상장된 종목인지 확인해주세요."
            )

    return wrapper

mcp = FastMCP(
    "Korean Stock Data",
    instructions="""한국 주식 데이터를 네이버 증권에서 실시간 조회합니다.
종목코드(예: 005930)나 종목명(예: 삼성전자)으로 검색할 수 있습니다.
차트 데이터, 투자자 수급, 재무지표, 시장 지수를 제공합니다.

## 차트 시각화 규칙

캔들 차트를 HTML Canvas로 렌더링할 때는 반드시 아래 레이아웃 구조를 따를 것.

### 영역 구분
- 전체 오른쪽 여백: PAD_R = AXIS_W + LABEL_W
- AXIS_W (≈ 42px): 차트 영역 바로 오른쪽. 세로 축선 + tick + 가격 숫자("XX만")만 표시
- LABEL_W (≈ 148px): AXIS_W 오른쪽. S/R 라벨명과 가격을 2줄로 좌측 정렬 표시
- 두 영역은 물리적으로 분리되어 절대 겹치지 않아야 함

### 패널 구성
- 캔들 패널: 전체 높이의 약 75% (상단)
- 거래량 패널: 전체 높이의 약 22% (하단), 캔들 패널과 GAP(≈ 10px) 간격
- 거래량 바 색상은 해당 봉의 상승/하락 색상과 동일하게 적용

### S/R 라벨 렌더링
- S/R 선은 캔들 패널 내 AXIS_X(= W - PAD_R) 까지만 그릴 것
- 라벨은 LABEL_X(= W - PAD_R + AXIS_W + 4) 기준 좌측 정렬
- 1행: 라벨명 (예: "강한 지지 (이중저점)")
- 2행: 가격 (예: "16.7만"), 1행보다 약간 작은 폰트 + 낮은 opacity

### 가격축
- 눈금선(grid)은 PAD_L ~ AXIS_X 구간에만 그릴 것
- tick은 AXIS_X에서 오른쪽으로 4px 짧게 표시
- 가격 숫자는 tick 바로 오른쪽(AXIS_X + 6px)에 표시
""",
)


@mcp.tool()
@safe_tool
async def search(query: str) -> str:
    """종목검색 — 종목명 또는 종목코드로 검색합니다.
    "삼성전자 종목코드", "반도체 관련주", "005930 뭐야" 같은 질문에 사용합니다.

    Args:
        query: 검색할 종목명 또는 코드 (예: "삼성전자", "005930")
    """
    results = await search_stock(query)
    if not results:
        return f"'{query}'에 대한 검색 결과가 없습니다."

    lines = [f"검색 결과 ({len(results)}건):"]
    for r in results:
        lines.append(f"  - {r['name']} ({r['code']})")
    return "\n".join(lines)


@mcp.tool()
@safe_tool
async def get_chart(code: str, timeframe: str = "day", count: int = 60) -> str:
    """차트데이터 — 종목의 OHLCV(시가/고가/저가/종가/거래량) 차트 데이터를 가져옵니다.
    "삼성전자 일봉", "차트 보여줘", "3개월 주봉", "월봉 데이터" 같은 질문에 사용합니다.

    Args:
        code: 종목코드 6자리 (예: "005930")
        timeframe: "day"(일봉), "week"(주봉), "month"(월봉)
        count: 가져올 봉 개수 (기본 60, 최대 500)
    """
    count = min(count, 500)
    data = await get_ohlcv(code, timeframe, count)
    if not data:
        return f"종목코드 {code}의 차트 데이터를 가져올 수 없습니다."

    tf_name = {"day": "일봉", "week": "주봉", "month": "월봉"}.get(timeframe, timeframe)
    lines = [f"종목 {code} {tf_name} 데이터 ({len(data)}개):", ""]
    lines.append("날짜 | 시가 | 고가 | 저가 | 종가 | 거래량")
    lines.append("---|---|---|---|---|---")
    for row in data:
        lines.append(
            f"{row['date']} | {row['open']:,} | {row['high']:,} | "
            f"{row['low']:,} | {row['close']:,} | {row['volume']:,}"
        )
    return "\n".join(lines)


@mcp.tool()
@safe_tool
async def get_price(code: str) -> str:
    """현재가 — 종목의 현재 시세 정보를 가져옵니다.
    "삼성전자 지금 얼마", "현재가", "오늘 시세", "주가 알려줘" 같은 질문에 사용합니다.

    Args:
        code: 종목코드 6자리 (예: "005930")
    """
    data = await get_current_price(code)
    if not data or "price" not in data:
        return f"종목코드 {code}의 현재가를 가져올 수 없습니다."

    lines = [
        f"종목: {data.get('name', code)} ({code})",
        f"현재가: {data['price']:,}원",
    ]
    if "change" in data:
        sign = "+" if data["change"] > 0 else ""
        lines.append(f"전일대비: {sign}{data['change']:,}원")
    if "open" in data:
        lines.append(f"시가: {data['open']:,}원")
    if "high" in data:
        lines.append(f"고가: {data['high']:,}원")
    if "low" in data:
        lines.append(f"저가: {data['low']:,}원")
    if "volume" in data:
        lines.append(f"거래량: {data['volume']:,}")
    return "\n".join(lines)


@mcp.tool()
@safe_tool
async def get_flow(code: str, days: int = 20) -> str:
    """투자자수급 — 투자자별 매매동향 (외국인/기관/개인 순매수량)을 가져옵니다.
    "외국인 수급", "기관 순매수", "수급 분석", "누가 사고 있어" 같은 질문에 사용합니다.

    Args:
        code: 종목코드 6자리 (예: "005930")
        days: 조회할 일수 (기본 20일)
    """
    days = min(days, 60)
    data = await get_investor_flow(code, days)
    if not data:
        return f"종목코드 {code}의 수급 데이터를 가져올 수 없습니다."

    lines = [f"종목 {code} 투자자별 매매동향 ({len(data)}일):", ""]
    lines.append("날짜 | 종가 | 거래량 | 기관 순매매 | 외국인 순매매")
    lines.append("---|---|---|---|---")
    for row in data:
        lines.append(
            f"{row['date']} | {row['close']:,} | {row['volume']:,} | "
            f"{row['institutional']:,} | {row['foreign']:,}"
        )

    # 합계
    total_inst = sum(r["institutional"] for r in data)
    total_frgn = sum(r["foreign"] for r in data)
    lines.append("")
    lines.append(f"합계 | - | - | {total_inst:,} | {total_frgn:,}")

    return "\n".join(lines)


@mcp.tool()
@safe_tool
async def get_financial(code: str) -> str:
    """재무지표 — 종목의 주요 재무지표(PER, PBR, 시가총액 등)를 가져옵니다.
    "PER", "PBR", "재무제표", "시가총액", "저평가" 같은 질문에 사용합니다.

    Args:
        code: 종목코드 6자리 (예: "005930")
    """
    data = await get_financials(code)
    if not data:
        return f"종목코드 {code}의 재무지표를 가져올 수 없습니다."

    lines = [f"종목: {data.get('name', code)} ({code})", ""]
    for key, value in data.items():
        if key in ("code", "name"):
            continue
        if isinstance(value, list):
            lines.append(f"{key}: {' | '.join(value)}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


@mcp.tool()
@safe_tool
async def get_index() -> str:
    """시장지수 — KOSPI, KOSDAQ 지수 현재값을 가져옵니다.
    "코스피", "코스닥", "시장 지수", "오늘 시장 어때" 같은 질문에 사용합니다.
    """
    data = await get_market_index()
    if not data:
        return "시장 지수를 가져올 수 없습니다."

    lines = ["시장 지수:"]
    for item in data:
        lines.append(f"  {item['index']}: {item.get('value', '-')} ({item.get('change', '-')})")
    return "\n".join(lines)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
