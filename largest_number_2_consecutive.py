
from typing import List
from typing import Tuple
from collections import Counter
class Reuben():
    def largest_number_2_years(self, nums: List[Tuple[int, int]]) -> int:
        diction = {year:freq for year, freq in nums}
        years = list(diction.keys())
        years_sorted = sorted(years)
        max_freq = 0
        for i in range(len(years_sorted)-1):
            freq_sum = diction[years_sorted[i]] + diction[years_sorted[i+1]]
            max_freq = max(max_freq, freq_sum)
        return max_freq

    def filter_out_stop_words(self, para: str, stop: List[str]) -> str:
        if not para:
            return null
        array = []
        for word in para:
            if word not in stop:
                array.append(word)
        word_counter = Counter(array)
        return word.counter.most_common(1)[0][0]

    def count_unique_elements_in_each_window(self, nums: List[int], k :int)-> List[int]:
        if not nums or k == 0:
            return []
        output = []
        for i in range(len(nums)-(k+1)):
            sub_array = nums[i:i+k]
            number = len(set(sub_array))
            output.append(number)
        return output
    def max_sum_of_window_size_k(self, nums: List[int], k: int)-> int:
        if not nums or k == 0:
            return "null"
        max_array = []
        for i in range(len(nums)-(k+1)):
            sub_array = nums[i:i+k]
            max_num = max(sub_array)
            max_array.append(max_num)
        return max(max_array)
    def nth_smallest(self, data: Dict[str,int], n: int) -> str:
        if not data or n > len(data.key()):
            return ""
        sorted_array = sorted(data.items(), key = lambda x: (-x[1],x[0]))
        return sorted_array[n-1]



obj = Reuben()
print(obj.largest_number_2_years([(2019,10),(2020,70),(2021,17),(2022,16)]))
print(obj.count_unique_elements_in_each_window([2,23,4,55,22,4,3,4,6,78,90],5))
# for i in range(4,8):
#     print(i)






