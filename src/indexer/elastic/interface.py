from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch


class ElasticsearchIndexer(ABC):
    """
    Abstract class for Elasticsearch indexing operations.

    This class defines the basic structure and required methods for indexing data
    into Elasticsearch. Concrete implementations should provide specific behavior
    for connecting to Elasticsearch, preparing data, and indexing.
    """

    def __init__(self, es_host: str, index_name: str):
        """
        Initialize the Elasticsearch indexer with connection settings and target index.

        :param es_host: The hostname or IP address of the Elasticsearch instance.
        :param index_name: The name of the Elasticsearch index where data will be stored.
        """
        self.es = Elasticsearch([es_host])
        self.index_name = index_name

    @abstractmethod
    def prepare_data(self, data):
        """
        Prepare data for indexing into Elasticsearch.

        This method should be implemented by concrete classes to transform raw data into
        a format suitable for Elasticsearch indexing.

        :param data: Raw data to be transformed and indexed.
        :return: Data formatted for Elasticsearch.
        """
        pass

    @abstractmethod
    def index_data(self, prepared_data):
        """
        Index prepared data into Elasticsearch.

        This method should be implemented by concrete classes to perform the actual
        indexing operation using the Elasticsearch client.

        :param prepared_data: Data that has been prepared for indexing.
        """
        pass

    @abstractmethod
    def create_index_if_not_exists(self, mappings):
        """
        Creates the Elasticsearch index with the specified mappings if it doesn't already exist.

        :param mappings: A dictionary defining the index mappings and settings.
        """
        pass
