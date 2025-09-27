# query/__init__.py
"""Pacote de comandos para eventos diários de cotação de CAD."""

from .quotes_usd_daily_event_query_repository import (
    QuotesUsdDailyEventQueryRepository as QuotesUsdDailyEventQueryRepository,
)

__all__ = ["QuotesUsdDailyEventQueryRepository"]
