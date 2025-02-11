"""
This module provides caching functionality for the LLM responses.
"""

from json import loads, dump
from os import path
from datetime import datetime, timedelta

class LLMCache():

    """
    Class to cache responses from the LLM model.
    """

    objects = 0

    def __init__(self, cache_time_window = 5):

        """
        Constructor for the LLMCache class.

        Args:
            cache_time_window (int): Time window for which the response is valid.
        """

        LLMCache.objects += 1
        LLMCache.__cache_path = path.join(path.dirname(__file__), 'cache.json')
        LLMCache.__cache = self.__load_cache()
        LLMCache.__garbage_collector(self)
        self.__cache_time_window = cache_time_window
        print("===========================================================")
        print(f"LLMCache object created. Total objects: {LLMCache.objects}")
        print("===========================================================")

    def __load_cache(self) -> dict:

        """
        Loads the cache from the cache file.
        """

        if path.exists(LLMCache.__cache_path):
            with open(LLMCache.__cache_path, 'r', encoding="utf-8") as f:
                return loads(f.read())
        return {}

    def __save_cache(self) -> None:

        """
        Writes the cache to the cache.json file.
        """

        with open(LLMCache.__cache_path, 'w', encoding="utf-8") as f:
            dump(LLMCache.__cache, f, indent=4)

    def __garbage_collector(self) -> None:

        """
        Deletes the expired cache entries.
        """

        current_time = self.__get_current_time()
        temp_cache = LLMCache.__cache.copy()
        for key in LLMCache.__cache:
            if not self.__is_valid_time(current_time, LLMCache.__cache[key]['valid_time']):
                del temp_cache[key]
        LLMCache.__cache = temp_cache
        self.__save_cache()

    def get_response(self, key: str) -> str | None:

        """
        Returns the response from the cache if it is valid.

        Args:
            key (str): Key to get the response from the cache

        Returns:
            str|None: Returns str if key is valid / not expired, else None
        """

        assert isinstance(key, str), "Key should be of type str"

        value = LLMCache.__cache.get(key, None)

        if value is None:
            return None

        if self.__is_valid_time(self.__get_current_time(), value['valid_time']):
            return value['response']

        return None

    def set_response(self, key: str, value: str) -> None:

        """
        Sets the response in the cache.

        Args:
            key (str): Key to store the response in the cache
            value (str): response to store in the cache
        """

        assert isinstance(key, str), "Messages should be of type str, do: str(messages)"
        assert isinstance(value, str), "Response should be of type str"

        current_time = self.__get_current_time()
        valid_time = self.__add_minutes_to_timestamp(current_time)
        LLMCache.__cache[key] = {'response': value, 'valid_time': valid_time}
        self.__save_cache()

    def __get_current_time(self) -> str:
        """Gets current time in the format: %Y-%m-%d %H:%M:%S"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __add_minutes_to_timestamp(self, timestamp: str) -> str:

        """
        Adds cache window minutes to the timestamp.
        Args:
            timestamp (str): Timestamp in the format: %Y-%m-%d %H:%M:%S
        Returns:
            str: Timestamp after adding cache window minutes
        """

        time_format = "%Y-%m-%d %H:%M:%S"
        time_obj = datetime.strptime(timestamp, time_format)
        new_time_obj = time_obj + timedelta(minutes = self.__cache_time_window)
        return new_time_obj.strftime(time_format)

    def __is_valid_time(self, timestamp1: str, timestamp2: str) -> bool:

        """
        Checks if timestamp1 is before timestamp2.

        Args:
            timestamp1 (str): Timestamp in the format: %Y-%m-%d %H:%M:%S
            timestamp2 (str): Timestamp in the format: %Y-%m-%d %H:%M:%S

        Returns:
            bool: True if timestamp1 is before timestamp2, else False
        """

        if timestamp1 > timestamp2:
            return False
        return True
