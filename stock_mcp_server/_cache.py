"""장중/장마감 차등 TTL 캐시.

한국 주식 시장은 평일 09:00~15:30 (KST)만 열린다.
장이 닫혀 있으면 데이터가 거의 변하지 않으므로 TTL을 길게 잡고,
장중에는 짧게 잡아서 신선도를 유지한다.

사용법:
    @cached(ttl_market=30, ttl_closed=3600)
    async def get_current_price(code: str) -> dict:
        ...
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime, time as dtime
from functools import wraps
from typing import Any, Callable, Awaitable
from zoneinfo import ZoneInfo

_KST = ZoneInfo("Asia/Seoul")
_MARKET_OPEN = dtime(9, 0)
_MARKET_CLOSE = dtime(15, 30)

_cache: dict[str, tuple[float, Any]] = {}
_lock = asyncio.Lock()


def is_market_open(now: datetime | None = None) -> bool:
    """현재 한국 주식 시장이 열려 있는지."""
    now = now or datetime.now(tz=_KST)
    # 월=0 ... 일=6
    if now.weekday() >= 5:
        return False
    t = now.time()
    return _MARKET_OPEN <= t <= _MARKET_CLOSE


def _make_key(func_name: str, args: tuple, kwargs: dict) -> str:
    parts = [func_name]
    parts.extend(repr(a) for a in args)
    parts.extend(f"{k}={v!r}" for k, v in sorted(kwargs.items()))
    return "|".join(parts)


def cached(
    ttl_market: int,
    ttl_closed: int | None = None,
):
    """async 함수 결과를 TTL 동안 캐싱.

    Args:
        ttl_market: 장 열려 있을 때 TTL (초)
        ttl_closed: 장 마감 후 TTL (초). None이면 ttl_market의 60배.
    """
    if ttl_closed is None:
        ttl_closed = ttl_market * 60

    def decorator(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = _make_key(func.__name__, args, kwargs)

            async with _lock:
                entry = _cache.get(key)
                if entry is not None:
                    expiry, value = entry
                    if time.time() < expiry:
                        return value
                    # 만료된 엔트리는 제거
                    del _cache[key]

            # 캐시 미스: 실제 함수 실행
            result = await func(*args, **kwargs)

            ttl = ttl_market if is_market_open() else ttl_closed
            async with _lock:
                _cache[key] = (time.time() + ttl, result)

            return result

        return wrapper

    return decorator


def clear_cache() -> None:
    """전체 캐시를 비운다 (테스트 / 수동 갱신용)."""
    _cache.clear()


def cache_stats() -> dict:
    """현재 캐시 상태 (디버깅용)."""
    now = time.time()
    active = sum(1 for exp, _ in _cache.values() if exp > now)
    return {
        "total_entries": len(_cache),
        "active_entries": active,
        "expired_entries": len(_cache) - active,
        "market_open": is_market_open(),
    }
