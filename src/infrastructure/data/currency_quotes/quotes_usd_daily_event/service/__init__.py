# service/__init__.py
"""Pacote de serviços para eventos diários de cotação de USD."""

from .quotes_usd_daily_event_service import (
    QuotesUsdDailyEventService as QuotesUsdDailyEventService,
)

__all__ = ["QuotesUsdDailyEventService"]
