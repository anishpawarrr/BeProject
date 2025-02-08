from json import loads, dump
from os import path
from datetime import datetime, timedelta

class LLMCache():

    objects = 0

    def __init__(self, cache_time_window = 5):
        LLMCache.objects += 1
        self.cache_path = path.join(path.dirname(__file__), 'cache.json')
        self.cache = self.__load_cache()
        self.__garbage_collector()
        self.cache_time_window = cache_time_window
        print("===========================================================")
        print(f"LLMCache object created. Total objects: {LLMCache.objects}")
        print("===========================================================")

    def __load_cache(self) -> dict:
        if path.exists(self.cache_path):
            with open(self.cache_path, 'r') as f:
                return loads(f.read())
        return {}
    
    def __save_cache(self):
        with open(self.cache_path, 'w') as f:
            dump(self.cache, f, indent=4)

    def __garbage_collector(self):
        current_time = self.__get_current_time()
        temp_cache = self.cache.copy()
        for key in self.cache:
            if not self.__is_valid_time(current_time, self.cache[key]['valid_time']):
                del temp_cache[key]
        self.cache = temp_cache
        self.__save_cache()

    def get_response(self, key):

        value = self.cache.get(key, None)

        if value is None:
            return None
        
        if self.__is_valid_time(self.__get_current_time(), value['valid_time']):
            return value['response']

        return None
        
    def set_response(self, key, value):
        current_time = self.__get_current_time()
        valid_time = self.__add_minutes_to_timestamp(current_time, self.cache_time_window)
        self.cache[key] = {'response': value, 'valid_time': valid_time}
        self.__save_cache()
    
    def __get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __add_minutes_to_timestamp(self, timestamp: str, minutes: int) -> str:
        time_format = "%Y-%m-%d %H:%M:%S"
        time_obj = datetime.strptime(timestamp, time_format)
        new_time_obj = time_obj + timedelta(minutes=minutes)
        return new_time_obj.strftime(time_format)
    
    def __is_valid_time(self, timestamp1: str, timestamp2: str) -> bool:
        if timestamp1 > timestamp2:
            return False
        return True

# llm_cache = LLMCache(cache_time_window=1)

# import llm
# promptp = "write a code to display hello world in python"
# promptc = "write a code to display hello world in c++"
# promptcs = "write a code to display hello world in c#"
# promptj = "write a code to display hello world in java"

# response = llm_cache.get_response(promptp)
# if response is None:
#     print("Response from model")
#     response = llm.get_response(promptp)
#     llm_cache.set_response(promptp, response)
# else:
#     print("Response from cache")
# print(response)