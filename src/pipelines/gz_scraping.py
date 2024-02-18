import time
from tqdm import tqdm
from src.utilis import save_to_json, load_from_json, check_and_create_dir, delete_file
from src.scraper import gz_scrapers
import os
import json


def extract_urls_recipes(output_dir: str, time_sleep: int, n_pages=440) -> list[str]:
    all_recipes_urls = load_from_json(f"{output_dir}/recipes_urls.json")
    if len(all_recipes_urls) == 0:
        ct_scraper = gz_scrapers.GZCategoriesScraper()
        categories_urls = ct_scraper.build_urls(n_pages=n_pages)
        all_recipes_urls = list()

        # Scrape category URLs to get recipe URLs
        for url in tqdm(categories_urls):
            try:
                recipes_urls = ct_scraper.scrape(url)
                all_recipes_urls.extend(recipes_urls)
            except Exception as e:
                print(f"An error occurred while scraping {url}: {e}")
            finally:
                time.sleep(time_sleep)

        # Save the scraped URLs to a JSON file
        save_to_json(list(set(all_recipes_urls)), f"{output_dir}/recipes_urls.json")

    return all_recipes_urls


def extract_recipes_info(all_recipes_urls: list[str], output_dir: str, time_sleep: int, n_files_already_processed: int):
    check_and_create_dir(f"{output_dir}/recipes_json")
    rec_scraper = gz_scrapers.GZRecipeScraper()

    all_recipes = list()
    chunk_n = 0
    for i, rec_url in enumerate(tqdm(all_recipes_urls)):
        try:
            recipe = rec_scraper.scrape(rec_url)
            all_recipes.append(recipe)
        except Exception as e:
            print(f"An error occurred while scraping {rec_url}: {e}")
        finally:
            time.sleep(time_sleep)

        # Save every 100 iterations and at the end
        if (i + 1) % 100 == 0 or i + 1 == len(all_recipes_urls):
            chunk_n += 1
            save_to_json(all_recipes, f'{output_dir}/recipes_json/all_recipes_{chunk_n + n_files_already_processed}.json')
            all_recipes = list()


def extract_links_from_json_dir(directory) -> (list[str], int):
    """
    Extract links from JSON files in the specified directory.

    Parameters:
    - directory (str): The directory containing JSON files.

    Returns:
    - list: A list of links extracted from the JSON files.
    """
    links = []
    n_files = 0
    try:
        for filename in os.listdir(directory):
            n_files += 1
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    for item in data:
                        if 'link' in item:
                            links.append(item['link'])
    except FileNotFoundError:
        pass
    return links, n_files


def run_pipeline(output_dir, time_sleep=2, n_pages=440, delete_cached_files=False):
    check_and_create_dir(output_dir)

    recipes_urls = extract_urls_recipes(output_dir, time_sleep, n_pages=n_pages)
    already_processed_recipes_urls, n_files = extract_links_from_json_dir(f"{output_dir}/recipes_json")
    recipes_urls = list(set(recipes_urls) - set(already_processed_recipes_urls))
    extract_recipes_info(recipes_urls, output_dir, time_sleep, n_files)

    if delete_cached_files:
        delete_file(f"{output_dir}/recipes_urls.json")
