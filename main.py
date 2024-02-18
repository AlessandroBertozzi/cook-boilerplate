from src.pipelines import gz_scraping

gz_scraping.run_pipeline('my_data', n_pages=1, delete_cached_files=False)
