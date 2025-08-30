"""Worker responsável por executar o ETL diário de cotação de BTC."""

from ...infrastructure.data.currency_quotes.quotes_btc_daily_event.query import (
    QuotesBtcDailyEventQueryRepository,
)
from ...infrastructure.data.currency_quotes.quotes_btc_daily_event.service import (
    QuotesBtcDailyEventService,
)

repository = QuotesBtcDailyEventQueryRepository(
    "https://api.coinbase.com/v2/prices/spot"
)
service = QuotesBtcDailyEventService(repository)

service.run()
