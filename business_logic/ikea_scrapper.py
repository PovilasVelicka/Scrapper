from typing import Generator, Optional

from interfaces.logger import ILogger
from interfaces.web_scrapper import IWebScrapper
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import json
import os


class IkeaScrapper(IWebScrapper):
    def __init__(self, url:str, logger: ILogger, headers: dict = None, time_delay: int = 2 ):
        """
        A web scraper for IKEA product listings.

        This class handles parsing the base URL, managing HTTP headers,
        applying a request delay, and maintaining scraping state across sessions.
        It uses a logger to track progress and errors.
        """
        parsed_url = urlparse(url)
        self.__logger = logger
        self.__base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        self.__rel_path = parsed_url.path
        self.__time_delay = time_delay
        self.__state_file = "ikea_scraper_state.json"
        self.__current_page = 1
        self.__current_item = 0
        if headers:
            self.__headers = headers
        else:
            self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "lt",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }


    def page_items(self) -> Generator[dict, None, None]:
        for item in self._get_all_items(self.__base_url + self.__rel_path):
            yield item


    def clear_state(self):
        if os.path.exists(self.__state_file):
            os.remove(self.__state_file)


    def _save_state(self):
        with open(self.__state_file, "w") as f:
            json.dump({
                "page_number": self.__current_page,
                "item_number": self.__current_item
            }, f)


    def _load_state(self):
        if os.path.exists(self.__state_file):
            with open(self.__state_file, "r") as f:
                data = json.load(f)
                self.__current_page = data.get("page_number", 1)
                self.__current_item = data.get("item_number", 0)


    def _get_all_items(self, url: str) -> Generator[dict, None, None]:
        self._load_state()

        while True:
            req_url = f"{url}?&product-room=product&page={self.__current_page}&order=RECOMMENDED"
            self.__logger.log_info(f"Processing page Nr.: {self.__current_page}, url: {req_url}")
            soup = self._get_soup(req_url)

            for i in self._get_page_items(soup):
                self.__logger.log_debug(f"Item {i['id']} complete")
                yield i
                self._save_state()

            page_counter = soup.select_one('span.showing_current_max')
            if page_counter:
                val = page_counter.text.strip().split()
                # Checks if the last number is a new maximum and a digit
                if val[-1].isdigit() and not any([x == val[-1] for x in val[:-1]]):
                    self.__current_page += 1
                    self.__current_item = 0
                    self._save_state()
                    continue
            break


    def _get_page_items(self, soup: BeautifulSoup) -> Generator[dict, None, None]:
        items = soup.select("#productFilterList > div > div.container.p-0 > div > div > div")
        start_index = self.__current_item

        for i in range(start_index, len(items)):
            a_tag = items[i].select_one("div.card-body > div.itemInfo.v2-b > a")
            description_tag = items[i].select_one("div.card-body > div.itemInfo.v2-b > h4")
            price_tag = items[i].select_one("div.itemPrice-wrapper p.itemNormalPrice span[data-price]")

            item = {
                "name": a_tag.get_text(strip=True) if a_tag else "",
                "description": description_tag.get_text(strip=True) if description_tag else "",
                "price": price_tag.get("data-price") if price_tag else "",
                "details": []
            }

            if a_tag:
                details_link = a_tag.get("href")
                d_soup = self._get_soup(self.__base_url + details_link)
                item["details"] = self._get_item_details(d_soup)
                item["id"] = self._get_item_id(d_soup)
            else:
                # Warn if item link is missing — likely means incomplete or malformed HTML
                self.__logger.log_warning(f"Item has no details {item}")

            self.__current_item = i  # Updates index to allow resuming from current position
            yield item


    @staticmethod
    def _get_item_details(d_soup: BeautifulSoup) -> list:
        item_details = []

        # Find the product size. PopUp window in web
        modal_size_tag = d_soup.select_one("#modal-product-size")
        if not modal_size_tag:
            return item_details  # Return empty list if the modal is not found

        # Find the first <tbody> within the modal
        first_table = modal_size_tag.select_one("tbody")
        if not first_table:
            return item_details  # Return empty list if no table is found

        # Select all rows in the table
        rows = first_table.select("tr")
        for row in rows:
            td = row.select("td")
            # Ensure the row has exactly two columns
            if len(td) == 2:
                key = td[0].text.strip().rstrip(":")  # Remove trailing colon
                value = td[1].text.strip()
                item_details.append({key: value})

        return item_details


    @staticmethod
    def _get_item_id(d_soup: BeautifulSoup) -> Optional[str]:
        modal_size_tag = d_soup.select_one("#modal-product-size")
        if modal_size_tag:
            id_tag = modal_size_tag.select_one("span.item-code")
            if id_tag:
                return id_tag.get_text(strip=True)
        return None


    def _get_soup(self, req_url: str) -> Optional[BeautifulSoup]:
        max_retries = 5
        for attempt in range(1, max_retries + 1):
            response = requests.get(req_url, headers=self.__headers)

            if 200 <= response.status_code < 300:
                time.sleep(self.__time_delay)
                return BeautifulSoup(response.content, 'html.parser')
            else:
                self.__logger.log_error(
                    f"[Attempt {attempt}] Failed to fetch URL: {req_url}, "
                    f"status code: {response.status_code}"
                )
                time.sleep(1)  # Delay before retrying

        # After all retries failed
        raise requests.HTTPError(
            f"Failed to retrieve content from {req_url} after {max_retries} attempts. "
        )