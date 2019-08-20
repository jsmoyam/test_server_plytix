import logging
from collections import defaultdict

from tools.decorators import log_function

logger = logging.getLogger('app')

class AnagramService:

    def __init__(self, words: list):
        self.anagrams = self._calculate_anagrams(words)

    @staticmethod
    def _calculate_anagrams(words: list) -> dict:
        """
        Get all anagrams from data source
        :param words: data source
        :return: dictionary with sorted string key and all words from datasource
        """

        # Create a dict with sorted words
        d = defaultdict(list)
        for word in words:
            key = ''.join(sorted(word))
            d[key].append(word)
        return d

    @log_function(logger)
    def get_anagram_words(self, word: str) -> list:
        """
        Return anagrams from word
        :param word: word to find anagrams
        :return: anagrams
        """

        # Order word alphabetically and find in dict
        sorted_word = ''.join(sorted(word))
        return self.anagrams.get(sorted_word, 'NO RESULTS')
