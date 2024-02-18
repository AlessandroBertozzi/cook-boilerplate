from src.indexer.elastic.interface import ElasticsearchIndexer
from dataclasses import dataclass
from typing import List


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    instructions: str


class MyElasticsearchIndexer(ElasticsearchIndexer):
    def prepare_data(self, data: Recipe):
        # Implement data preparation logic here
        return data

    def index_data(self, prepared_data):
        # Implement data indexing logic here
        for record in prepared_data:
            self.es.index(index=self.index_name, document=record)

    def create_index_if_not_exists(self, mappings):
        """
        Checks if the specified index exists, and creates it with the provided mappings if it does not.

        :param mappings: A dictionary containing the Elasticsearch index mappings and settings.
        """
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=mappings)
            print(f"Index '{self.index_name}' created.")
        else:
            print(f"Index '{self.index_name}' already exists.")
