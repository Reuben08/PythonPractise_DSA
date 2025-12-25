


# from typing import List
#
# class Reuben():
#     def two_sum(self, nums: List[int], K: int) -> List[int]:
#         seen = {}
#         for i, num in enumerate(nums):
#             diff = K - num
#             if diff in seen:
#                 return [seen[diff],i]
#             else:
#                 seen[num] = i
#         return []
#
#     def count_even_odd(nums: List[int]) -> Tuple[int, int]:
#         if not nums:
#             return 0,0
#         even_count = []
#         odd_count = []
#         for num in nums:
#             if num % 2  == 0:
#                 even_count.append(num)
#             else:
#                 odd_count.append(num)
#         even_len = len(event_count)
#         odd_len = len(odd_count)
#         return even_len,odd_len
#
#     def most_frequent_number(nums: List[int]) -> int:
#         if not nums:
#             return 0
#         counter_nums = Counter(nums)
#         sorted_nums = sorted(counter_nums.items(), key = lambda x:(-x[1],x[0]))
#         return sorted_nums[0][0]
#
#     def find_duplicates(self, nums: List[int]) -> List[int]:
#         if not nums:
#             return [0]
#         output = []
#         num_counter = Counter(nums)
#         for num, freq in num_counter.items():
#             if freq > 1:
#                 output.append(nums)
#         return output if len(output) > 0 else []
#
# obj = Reuben()
# print(obj.two_sum([2,3,4,5,7],11))
#
# list1 = [123,3,4,5,6,23423,234]
# num = max(list1)
# print(num)

from typing import List, Tuple
from collections import defaultdict

def top3_books_by_category(books_points: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    if not books_points:
        return []
    category_max = defaultdict(int)
    for category, points in books_points:
        category_max[category] = max(category_max[category], points)

    sorted_cats = sorted(category_max.items(), key=lambda x: x[1], reverse=True)

    return sorted_cats[:3]

print(top3_books_by_category([
    ('Vaishali',10),('Kanika',10),('Reuben',10),('Vaishali',15),('Raghu',10),('Vaishali',10)
]))


