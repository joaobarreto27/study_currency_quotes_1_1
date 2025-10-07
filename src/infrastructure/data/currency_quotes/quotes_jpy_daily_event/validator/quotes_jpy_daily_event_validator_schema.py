"""Validação para o schema de eventos de cotação de JPY."""

from datetime import datetime

from pydantic import BaseModel, PositiveFloat


class QuotesJpyDailyEventValidatorSchema(BaseModel):
    """Schema de validação para os eventos de cotação de JPY."""

    code: str
    codein: str
    name: str
    high: PositiveFloat
    low: PositiveFloat
    varBid: float
    pctChange: float
    bid: PositiveFloat
    ask: PositiveFloat
    timestamp: int
    create_date: datetime
