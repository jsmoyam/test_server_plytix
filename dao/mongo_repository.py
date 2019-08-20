import logging

from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError

from app_exception import AppException, GenericErrorMessages
from tools.decorators import log_function

logger = logging.getLogger('app')


class MongoRepository:

    def __init__(self, connection_url: str) -> None:
        """
        Constructor with url connection
        :param connection_url: url connection from ini file
        :type connection_url: str
        :return: This function return nothing
        :rtype: None
        """

        self.connection_url = connection_url
        self.schema = connection_url.split('/')[-1]

        try:
            # Connect with mongodb
            self.connection = self.open_connection()

            # Get database from URL connection
            self.db = self.connection.get_database()

            # Get collection. Create if not exist
            if self.schema not in self.db.collection_names():
                self.db.create_collection(self.schema)
            self.mongo_collect = self.db[self.schema]

        except errors.ConfigurationError:
            raise AppException(GenericErrorMessages.CONFIGURATION_ERROR)
        except AppException as e:
            raise e

    @log_function(logger)
    def fill_database(self, data: list):
        """
        Fill database with data. Delete old data
        :param data: test data
        :return: bool
        """
        self.mongo_collect.drop()
        self.mongo_collect.insert(data)
        return True

    @log_function(logger)
    def get_words_list(self) -> list:
        """
        Get words from database and convert to list
        :return: words from database as list
        """

        output = list()
        db_words = self.get_words()

        for db_word in db_words:
            output.append(db_word['word'])

        return output

    @log_function(logger)
    def get_words(self) -> list:
        """
        Get words from database
        :return: words list
        """

        try:
            return list(self.mongo_collect.find({}, {'_id': False}))
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    @log_function(logger)
    def store_words(self, words: list) -> bool:
        """
        Store words to dabaase
        :param words: words from client
        :return: boolean
        """

        # Drop collection and insert. If there are a lot words then an attribute 'position' must be used
        try:
            self.mongo_collect.drop()
            self.mongo_collect.insert(words)
            return True
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def open_connection(self) -> None:
        """
        Get the connection whith mongodb and check that it is successful.
        :return: object that represents the connection
        :rtype: object
        """

        try:
            connection = MongoClient(self.connection_url)
            connection.is_mongos
            return connection

        except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError):
            raise AppException(GenericErrorMessages.DATABASE_ERROR)
