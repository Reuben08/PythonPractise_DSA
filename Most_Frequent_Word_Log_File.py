

import re
from typing import List
from collections import Counter

class Reuben():
    def most_frequent_word(self, logs: List[str], stop_words: List[str]) -> str:
        log_array = []
        for string in logs:
            cleaned_string = re.sub(r'[^\w\s]','',string.lower())
            print("start " + cleaned_string + "  end")
            log_array.extend(cleaned_string.split())
        final_array = []
        for word in log_array:
            if word not in stop_words:
                final_array.append(word)
        final_counter = Counter(final_array)
        return final_counter.most_common(1)[0][0]

    def unique_elements_sliding_window(self, nums: List[int], k: int) -> List[int]:
        if not nums:
            return []
        final_array = []
        for i in range(len(nums)-k+1):
            temp_arr = nums[i:i+k]
            count = len(set(temp_arr))
            final_array.append(count)
        return final_array
    def flatten_and_merge(self, data: dict[str, List[str]]) -> List[str]:
        if not data:
            return []
        list_1 = data["A"]
        list_2 = data["B"]
        final_array = []
        for a,b in zip(list_1,list_2):
            final_array.append(a+b)
            return final_array

    def key_with_nth_value(self, input_dict: dict[str, int], n: int)-> str:
        if not input_dict:
            return ""
        List_values = list(input_dict.values())
        List_values.sorted()
        nth_value = List_values[n-1]
        for key,value in input_dict.items():
            if value == nth_value:
                return key
        return ""
    def fist_timestamp_user(self, logs: List[dict[str,str]])-> dict[str,str]:
        if not logs:
            return {}
        timestamp_user = defaultdict


