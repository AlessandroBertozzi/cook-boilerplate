from src.interface.scraper import Scraper
import requests
from bs4 import BeautifulSoup
import re


class GZRecipeScraper(Scraper):
    """
    A scraper class for extracting detailed recipe information from web pages.
    Inherits from the Scraper base class.
    """

    def fetch_data(self, url):
        """
        Fetches the HTML content of the specified URL.

        :param url: URL of the web page to scrape.
        :return: Raw HTML content of the web page as a string.
        """
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful.
        return response.text

    def parse_data(self, raw_data):
        """
        Parses the raw HTML content to extract structured recipe data.

        :param raw_data: Raw HTML content of a web page.
        :return: A dictionary containing the structured data of a single recipe.
        """
        single_recipe = dict()
        soup = BeautifulSoup(raw_data, 'lxml')
        single_recipe['recipe'] = self.name(soup)
        single_recipe['ingredients'] = self.extract_ingredients(soup)
        single_recipe['category'] = self.extract_categories(soup)
        single_recipe['difficulty'] = self.infobox(soup)['difficoltà']
        single_recipe['dosage_for'] = self.infobox(soup)['dosi per']
        single_recipe['price'] = self.infobox(soup)['costo']
        single_recipe['time'] = {
            'preparation': self.infobox(soup)['preparazione'],
            'cooking': self.infobox(soup)['cottura']
        }
        single_recipe['steps'] = self.steps(soup)
        single_recipe['link'] = self.url
        return single_recipe

    def store_data(self, data):
        """
        Placeholder method for storing scraped data. Currently does nothing.

        :param data: The data to store.
        """
        pass  # Implement data storage logic here.

    @staticmethod
    def name(recipe_soup):
        """
        Extracts the recipe name from the soup object.

        :param recipe_soup: BeautifulSoup object representing the parsed HTML of a recipe page.
        :return: Recipe name as a string.
        """
        tag = recipe_soup.find("h1", {"class": "gz-title-recipe gz-mBottom2x"}).text.lower()
        return tag

    @staticmethod
    def extract_categories(recipe_soup):
        """
        Extracts the recipe category from the soup object.

        :param recipe_soup: BeautifulSoup object representing the parsed HTML of a recipe page.
        :return: Recipe category as a string.
        """
        categories = list()
        tag = recipe_soup.find("div", {"class": "gz-title-content gz-innerdesktop"})
        if tag:
            tag = [cat.lower() for cat in tag.div.ul.li.text.strip().lower().split('\n') if cat != '']
            tag = list(set(tag))
            categories.extend(tag)
        infos_categories = recipe_soup.find("div", {"class": "gz-list-featured-data-other"})
        if infos_categories:
            infos_categories = [cat.lower() for cat in infos_categories.text.strip().split('\n') if cat != '']
            categories.extend(infos_categories)
        return categories

    @staticmethod
    def extract_quantity_unit_enhanced(text):
        """
        Enhanced function to extract the quantity and the rest of the text from a given string,
        including cases where the number might come after text within parentheses.

        :param text: String containing the quantity and possibly a unit or other descriptive text.
        :return: A dictionary with keys 'quantity', 'unit_measure', and 'strange_measure'.
        """
        # List of known cooking units for comparison
        known_units = [
            'tsp', 'tbsp', 'fl oz', 'c', 'pt', 'qt', 'gal', 'ml', 'l',
            'oz', 'lb', 'g', 'kg', 'cl', 'cm', 'm'
        ]

        # Regular expression to match the number and the following text, including parentheses
        pattern = re.compile(r'(\d+\.?\d*)\s*(\w+)?|(\(\w+\))(\d+\.?\d*)')
        matches = pattern.findall(text.lower())

        # Initialize default values
        quantity = None
        measure = None

        for match in matches:
            if match[0]:  # Number before text
                quantity = match[0]
                measure = match[1]
            elif match[3]:  # Number after parentheses
                quantity = match[3]
                measure = match[2].strip('()')  # Remove parentheses

        if measure and measure.lower() in known_units:
            return {'amount': quantity, 'standard_unit': measure, 'descriptor': None}
        else:
            return {'amount': quantity, 'standard_unit': None, 'descriptor': measure}

    @staticmethod
    def steps(recipe_soup):
        """
        Extracts the cooking steps from the soup object.

        :param recipe_soup: BeautifulSoup object representing the parsed HTML of a recipe page.
        :return: Dictionary of cooking steps, indexed by step number.
        """
        steps = dict()
        all_recipes_tag = recipe_soup.find_all("div", {"class": "gz-content-recipe-step"})
        for i, recipe_name in enumerate(all_recipes_tag):
            list_tag_remove = recipe_name.find_all("span", {"class": "num-step"})
            for tag in list_tag_remove:
                tag.extract()
            # Remove extra spaces and fix spacing around punctuation
            cleaned_text = ' '.join(recipe_name.p.text.split())  # Remove extra spaces
            cleaned_text = (cleaned_text
                            .replace(' ,', ',')
                            .replace(' .', '.')
                            .replace(' ;', ';')
                            .replace(' :', ':'))
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            steps[i] = cleaned_text
        return steps

    def extract_ingredients(self, recipe_soup):
        """
        Extracts ingredients and their quantities from the soup object.

        :param recipe_soup: BeautifulSoup object representing the parsed HTML of a recipe page.
        :return: Dictionary of ingredients and their respective quantities.
        """
        ingredients = list()
        already_parsed_ingredient = list()
        all_recipes_tag = recipe_soup.find_all("dd", {"class": "gz-ingredient"})
        for recipe_name in all_recipes_tag:
            name = recipe_name.a.text.strip().replace("\t", "").replace("\n", "").lower()
            if name not in already_parsed_ingredient:
                already_parsed_ingredient.append(name)
                ingredient = {
                    "name": name,
                    "quantity": self.extract_quantity_unit_enhanced(
                        recipe_name.span.text.strip().replace("\t", "").replace("\n", ""))
                }
                ingredients.append(ingredient)
        return ingredients

    @staticmethod
    def infobox(recipe_soup):
        """
        Extracts infobox data like cooking time, difficulty level, etc., from the soup object.

        :param recipe_soup: BeautifulSoup object representing the parsed HTML of a recipe page.
        :return: Dictionary of infobox data.
        """
        all_infos_clean = list()
        all_infos = recipe_soup.find_all("span", {"class": "gz-name-featured-data"})
        for info in all_infos:
            single_data = [i.strip().lower() for i in info.text.split(':')]
            if len(single_data) > 1 and single_data not in all_infos_clean:
                all_infos_clean.append(single_data)

        infos_dict = {
            "difficoltà": None,
            "preparazione": None,
            "cottura": None,
            "dosi per": None,
            "costo": None
        }
        for info in all_infos_clean:
            if info[0] == 'difficoltà':
                infos_dict['difficoltà'] = info[1]
            elif info[0] == 'preparazione':
                infos_dict['preparazione'] = info[1]
            elif info[0] == 'cottura':
                infos_dict['cottura'] = info[1]
            elif info[0] == 'costo':
                infos_dict['costo'] = info[1]
            elif info[0] == 'dosi per':
                infos_dict['dosi per'] = info[1]

        return infos_dict


class GZCategoriesScraper(Scraper):
    """
    A scraper class for extracting URLs of recipes from a category page.
    Inherits from the Scraper base class.
    """

    def fetch_data(self, url):
        """
        Fetches the HTML content of the specified category URL.

        :param url: URL of the category page to scrape.
        :return: Raw HTML content of the category page as a string.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_data(self, raw_data):
        """
        Parses the raw HTML content to extract a list of recipe URLs from the category page.

        :param raw_data: Raw HTML content of a category page.
        :return: List of recipe URLs found on the category page.
        """
        list_urls = list()
        soup = BeautifulSoup(raw_data, 'lxml')
        all_recipes_tag = soup.find_all("h2", {"class": "gz-title"})
        for recipe_tag in all_recipes_tag:
            recipe_url = recipe_tag.a['href']
            list_urls.append(recipe_url)
        return list_urls

    def store_data(self, data):
        """
        Placeholder method for storing scraped data. Currently does nothing.

        :param data: The data to store.
        """
        pass

    @staticmethod
    def build_urls(base_url='https://www.giallozafferano.it/ricette-cat', n_pages=10):
        """
        Method for generating urls for request

        :param base_url: The base url of the website Giallo Zafferano.
        :param n_pages: The number of pages to parse.
        """
        all_urls = list()

        all_urls.append(f"{base_url}")
        for page in range(1, n_pages + 1):
            all_urls.append(f"{base_url}/page{page}")

        return all_urls
