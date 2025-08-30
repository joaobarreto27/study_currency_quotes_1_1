"""Worker responsável por executar o ETL diário de cotação de BTC."""

from ...infrastructure.data.currency_quotes.quotes_btc_daily_event.command import (
    QuotesBtcDailyEventCommandRepository,
)
from ...infrastructure.data.currency_quotes.quotes_btc_daily_event.service import (
    QuotesBtcDailyEventService,
)

repository = QuotesBtcDailyEventCommandRepository("https://exemplo.com/api")
service = QuotesBtcDailyEventService(repository)

service.run()
