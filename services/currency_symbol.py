from currency_symbols import CurrencySymbols
from currency_symbols._constants import CURRENCY_SYMBOLS_MAP  # noqa


SYMBOLS_CURRENCY_MAP = {item: key for key, item in CURRENCY_SYMBOLS_MAP.items()}
SYMBOLS_CURRENCY_MAP["$"] = "USD"
SYMBOLS_CURRENCY_MAP["£"] = "GBP"



class CustomCurrencySymbols(CurrencySymbols):
    @staticmethod
    def get_currency(symbol: str) -> str | None:
        return SYMBOLS_CURRENCY_MAP.get(symbol, None)
