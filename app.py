from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from app_config import AppConfig
from app_exception import AppException
from dao.mongo_repository import MongoRepository
from services.anagram_service import AnagramService
from tools.decorators import log_function

# Define flask, cors, config and logger
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
config = AppConfig()
logger = config.get_log('app')

# Connect to database
db = MongoRepository(config.get_value('app', 'connection_database'))

# Init service
words = db.get_words_list()
anagram_service = AnagramService(words)


@app.route('/api/testdata')
def fill_database():
    """
    Fill database with data test
    :return: 200 ok or exception
    """

    try:
        data = [{'word': 'foo'}, {'word': 'bar'}, {'word': 'xyzzy'}]
        db.fill_database(data)
        return Response(status=200)
    except AppException as e:
        logger.error(str(e))


@app.route('/api/words')
@log_function(logger)
def get_words():
    """
    Get words from database
    :return: words as json or exception
    """

    try:
        return jsonify(db.get_words())
    except AppException as e:
        logger.error(str(e))


@app.route('/api/store', methods=['POST'])
@log_function(logger)
def store():
    """
    Store data to database
    :return: 200 ok or exception
    """

    try:
        data = request.json
        db.store_words(data)
        return Response(status=200)
    except AppException as e:
        logger.error(str(e))


@app.route('/api/anagrams', methods=['POST'])
def get_anagrams():
    """
    Get anagrams in database from word
    :return: json or exception
    """

    try:
        word = request.data.decode('utf-8')
        return jsonify(anagram_service.get_anagram_words(word))
    except AppException as e:
        logger.error(str(e))


if __name__ == '__main__':
    app.run()
