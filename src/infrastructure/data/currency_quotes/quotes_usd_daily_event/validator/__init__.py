# validator/__init__.py
"""Pacote de validação para eventos de cotação de USD."""

from .quotes_usd_daily_event_validator import (
    QuotesUsdDailyEventValidatorSchema as QuotesUsdDailyEventValidatorSchema,
)

__all__ = ["QuotesUsdDailyEventValidatorSchema"]
