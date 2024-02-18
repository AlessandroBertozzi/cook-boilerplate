from src.interface.elastic import ElasticsearchIndexer
from dataclasses import dataclass
from typing import List
from elasticsearch.helpers import bulk


@dataclass
class Quantity:
    amount: str | None
    standard_unit: str | None
    descriptor: str | None


@dataclass
class Ingredient:
    name: str
    quantity: Quantity


@dataclass
class Time:
    preparation: str
    cooking: str


@dataclass
class Recipe:
    recipe: str
    ingredients: List[Ingredient]
    category: list[str]
    difficulty: str
    dosage_for: str
    price: str
    time: Time
    steps: dict[str: str]
    link: str


class MyElasticsearchIndexer(ElasticsearchIndexer):
    def _prepare_data(self, data: Recipe):
        # Implement data preparation logic here
        return data

    def _format_for_bulk_indexing(self, documents):
        """
        Formats a list of documents for bulk indexing in Elasticsearch.

        :param documents: List of document dictionaries to be indexed.
        :return: A generator that yields properly formatted bulk API actions.
        """
        for doc in documents:
            yield {
                "_index": self.index_name,
                "_source": doc
            }

    def index_data(self, data: Recipe):
        record = self._prepare_data(data)
        self.es.index(index=self.index_name, document=record)

    def bulk_data(self, documents):
        # Executing bulk indexing
        success, _ = bulk(self.es, self._format_for_bulk_indexing(documents))
        print(f"Successfully indexed {success} documents.")

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
