from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any


def ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def to_float(value: Any, *, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def top_products_from_orders(orders: list[dict[str, Any]], *, limit: int = 3) -> list[str]:
    counter: Counter[str] = Counter()
    for order in orders:
        product_name = order.get("product")
        if isinstance(product_name, str) and product_name.strip():
            counter[product_name.strip()] += 1
    return [name for name, _ in counter.most_common(limit)]
