import json
import urllib.request
from html.parser import HTMLParser


class USDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.right_row = False
        self.cells_to_rate = 3
        self.rate = None

    def error(self, message: str) -> None:
        pass

    def handle_starttag(self, tag: str, attrs: list):
        if self.right_row and tag == "td":
            self.cells_to_rate -= 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr":
            self.right_row = False
            self.cells_to_rate = 3

    def handle_data(self, data: str) -> None:
        if data == "USD":
            self.right_row = True
        if not self.cells_to_rate:
            rate = float(data.replace(",", "."))
            self.rate = rate
            self.right_row = False
            self.cells_to_rate = 3


def get_external_page_with_rates() -> str:
    with urllib.request.urlopen("https://www.cbr.ru/currency_base/daily/") as response:
        return response.read().decode()


def index(*args, **kwargs) -> str:
    try:
        usd_amount = float(kwargs["usd_amount"][0])
    except ValueError:
        result = {
            "error": "usd_amount must be a number",
        }
        return json.dumps(result)
    except KeyError:
        result = {
            "error": "usd_amount is required",
        }
        return json.dumps(result)
    html = get_external_page_with_rates()
    parser = USDParser()
    parser.feed(html)
    result = {
        "usd_rur_rate": parser.rate,
        "usd_amount": usd_amount,
        "rur_amount": parser.rate * usd_amount,
    }
    return json.dumps(result)

