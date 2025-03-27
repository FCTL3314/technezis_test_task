import requests
from parsel import Selector
from price_parser import Price


async def parse_price(url: str, xpath: str) -> Price | None:
    try:
        response = requests.get(url, timeout=5)
        if not response.ok:
            return None
        selector = Selector(response.text)
        price = selector.xpath(xpath).get()
        if isinstance(price, str):
            try:
                return Price.fromstring(price)
            except Exception as e:
                print(f"Error during price string parsing: {e}")
                return None
        return None
    except Exception as e:
        print(f"Error during price request: {e}")
        return None