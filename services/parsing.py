import requests
from parsel import Selector


async def parse_price(url: str, xpath: str) -> str | None:
    try:
        response = requests.get(url, timeout=5)
        if not response.ok:
            return None
        selector = Selector(response.text)
        price = selector.xpath(xpath).get()
        return price.strip() if price else None
    except Exception as e:
        print(f"Unable: {e}")
        return None