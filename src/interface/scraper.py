from abc import ABC, abstractmethod


class Scraper(ABC):

    def __init__(self):
        self.url = None

    @abstractmethod
    def fetch_data(self, url):
        """
        Fetch data from the given URL.

        :param url: The URL to fetch data from.
        """
        pass

    @abstractmethod
    def parse_data(self, raw_data):
        """
        Parse the fetched data.

        :param raw_data: The raw data to parse.
        :return: Parsed data in a structured format.
        """
        pass

    @abstractmethod
    def store_data(self, data):
        """
        Store the parsed data.

        :param data: The structured data to be stored.
        """
        pass

    def scrape(self, url):
        """
        The main method to orchestrate the scraping process.

        :param url: The URL to scrape data from.
        """
        raw_data = self.fetch_data(url)
        self.url = url
        data = self.parse_data(raw_data)
        self.store_data(data)
        return data
