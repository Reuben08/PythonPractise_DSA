# from typing import List
#
# def reverse_array(arr) -> List[int]:
#     if not arr:
#         return []
#     left, right = 0, len(arr)-1
#     while left < right:
#         arr[left],arr[right] = arr[right],arr[left]
#         left += 1
#         right -= 1
#     return arr
# def return_sorted(arr) -> List[int]:
#     if not arr:
#         return []
#     return sorted(arr)
#
# def two_sum(arr: List[int], target: int) -> List[int]:
#     if not arr:
#         return []
#     seen = {}
#     for i,num in enumerate(arr):
#         diff = target - num
#         if diff in seen:
#             return [seen[diff], i]
#         seen[num] = i
#     return []
#
# from collections import defaultdict
#
# def first_unique_element(arr) -> int:
#     if not arr:
#         return null
#     num_counter = defaultdict(int)
#     for i in arr:
#         num_counter[i] += 1
#     for x in arr:
#         if num_counter[x] == 1:
#             return x
#     return -1

from collections import Counter, defaultdict
# from typing import List
#
# def anagram_check(s1: str, s2: str) -> bool:
#     if not s1 or not s2:
#         return False
#     s1_counter = Counter(s1)
#     s2_counter = Counter(s2)
#     if s1_counter == s2_counter:
#         return True
#     return False
#
#
# def sub_array_sum(arr: List[int], k: int) -> int:
#     if not arr:
#         return null
#     prefix_sum = 0
#     count = 0
#     freq = defaultdict(int)
#     freq[0] = 1
#     for num in arr:
#         prefix_sum += num
#         if prefix_sum-k in freq:
#             count += freq[prefix_sum-k]
#         freq[prefix_sum] += 1
#
#     return count
#
# # print(reverse_array([1,2,3,4,5,6]))
# # print(return_sorted([123,213,2,42,123,-12,2,323]))
# # print(two_sum([2,5,7,8,9],7))
# # print(first_unique_element([1,1,2,3,4,4,2]))
# # print(anagram_check("listen","silent"))
# # print(sum([1,2,3,4]))
#
#
# print(sub_array_sum([1,1,1,1,1,1,1],3))
#
# from typing import List
#
# def return_positive_arr(arr: List[int]) -> int:
#     if not arr:
#         return 0
#     sorted_arr = sorted(x for x in arr if x>= 0)
#     return sorted_arr
#
# print(return_positive_arr([-9,-8,-7,-4,2,3,4,5,6]))

# from collections import Counter
#
# def return_top_k(num: List[int], k:int) -> List[int]:
#     if not num:
#         return []
#     num_counter = Counter(num)
#     return num_counter.most_common(k)[0][0]

# print({1,3,4} & {1})

# from typing import List
#
# def longest_consec_sequence(nums: List[int]) -> int:
#     if not nums:
#         return 0
#     Intset = set(nums)
#     longest = 0
#     res = []
#     for num in nums:
#         if (num-1) not in Intset:
#             length = 1
#             while num + length in Intset:
#                 length += 1
#             if length > longest:
#                 longest = length
#     return longest
#
# print(longest_consec_sequence([1,2,3,4,1123,12312123,123,12,21,5,12,13,14]))


from collections import defaultdict
from typing import List

# def prefix_sum_arr(nums: List[int], k: int) -> int:
#     if not nums:
#         return 0
#     if not k:
#         return 0
#     prefix_sum = 0
#     freq = defaultdict(int)
#     freq[0] = 1
#     count = 0
#     for num in nums:
#         prefix_sum += num
#         if (prefix_sum-k) in freq:
#             count += freq[prefix_sum-k]
#         freq[prefix_sum] += 1
#     return count
#
# print(prefix_sum_arr([1,1,1,1,1,1,1,1],3))


# from collections import defaultdict
#
# def longest_k_distinct_char(s: str, k:int) -> int:
#     if not s:
#         return 0
#     if not k:
#         return 0
#     l = 0
#     max_len = 0
#     freq = defaultdict(int)
#     for r, char in enumerate(s):
#         freq[char]  += 1
#
#         while len(freq) > k:
#             char_left = s[l]
#             freq[char_left] -= 1
#             if freq[char_left] == 0:
#                 del freq[char_left]
#             l += 1
#         max_len = max(max_len, r - l +1)
#     return max_len
#
#
# print(longest_k_distinct_char("eceeeeeeeeeeba",2))
#
# array = [1,2,3,4,5,6,7,8,9]
# # rev = sorted(array, reverse = True)
# # print(rev)
# print(array[::-1])

#
# def rotate(nums: List[int], k: int) -> None:
#     """
#     Do not return anything, modify nums in-place instead.
#     """
#     if not nums:
#         return None
#     n = len(nums)
#     k = k % n  # handle k > n
#     return (nums[-k:] + nums[:-k])
# print(rotate([-1,-100,3,99],2))


# def valid_paranthesis(s: str) -> bool:
#     if not s:
#         return False
#     stack = []
#     mapping = {')': '(', '}': '{', ']': '['}
#     for char in s:
#         if char in mapping.values():
#             stack.append(char)
#         elif char in mapping:
#             if not stack or stack[-1] != mapping[char]:
#                 return False
#             stack.pop()
#     return not stack
#
# print(valid_paranthesis("()[]["))

from typing import List
# from collections import defaultdict
#
#
# def longest_palindromic_substring(s: str) -> str:
#     if not s:
#         return ""
#
#     word_map = defaultdict(dict)
#     longest = 0
#     longest_word = ""
#
#     for i in range(len(s)):
#         # Odd-length palindromes
#         l, r = i, i
#         while l >= 0 and r < len(s) and s[l] == s[r]:
#             current_word = s[l:r + 1]
#             word_map[(l, r)] = {"length": r - l + 1, "substring": current_word}
#             if len(current_word) > longest:
#                 longest = len(current_word)
#                 longest_word = current_word
#             l -= 1
#             r += 1
#
#         # Even-length palindromes
#         l, r = i, i + 1
#         while l >= 0 and r < len(s) and s[l] == s[r]:
#             current_word = s[l:r + 1]
#             word_map[(l, r)] = {"length": r - l + 1, "substring": current_word}
#             if len(current_word) > longest:
#                 longest = len(current_word)
#                 longest_word = current_word
#             l -= 1
#             r += 1
#
#     return longest_word, longest, word_map
#
# result, length, mapping = longest_palindromic_substring("babad")
# print("Longest:", result)
# print("Length:", length)
# print("All palindromes:", mapping)

# def longest_substring(s: str) -> int:
#     if not s:
#         return 0
#     charset = set()
#     l = 0
#     longest = 0
#     for r in range(len(s)):
#         while s[r] in charset:
#             charset.remove(s[l])
#             l += 1
#         charset.add(s[r])
#         longest = max(longest, r - l + 1)
#     return longest
#
# print(longest_substring("abcdecaaaaa"))

# from collections import defaultdict
#
# def longest_substring_with_atmost_k(s: str, k: int) -> dict:
#     if not s or k > len(s):
#         return ""
#     char_counter = defaultdict(int)
#     l = 0
#     longest = 0
#     for r in range(len(s)):
#         char_counter[s[r]] += 1
#         while len(char_counter) > k:
#             char_counter[s[l]] -= 1
#             if char_counter[s[l]] == 0:
#                 char_counter.pop(s[l])
#             l += 1
#         if r - l + 1 > longest:
#             longest = r - l + 1
#             start = l
#
#     return s[start: start + longest]
#
# print(longest_substring_with_atmost_k("aaaaaaaaaaaabc",2))
#
# import itertools
#
# my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# k = 3
#
# first_k_items = dict(itertools.islice(my_dict.items(), k))
# print(first_k_items)

#
# my_dict = {'apple': 1, 'banana': 2, 'cherry': 3, 'date': 4, 'elderberry': 5}
# k = 3
#
# first_k_keys = list(my_dict.keys())[:k]
# print(first_k_keys)

#
# def longest_substring_with_atmost_k_char(s: str, k: int) -> str:
#     if not s or k == 0:
#         return ""
#     longest = 0
#     output = ""
#     char_counter = defaultdict(int)
#     l = 0
#     for r in range(len(s)):
#         char_counter[s[r]] += 1
#         while len(char_counter) > k:
#             char_counter[s[l]] -= 1
#             if char_counter[s[l]] == 0:
#                 del char_counter[s[l]]
#             l+=1
#         if r - l + 1 > longest:
#             longest = r - l + 1
#             output = s[l:r+1]
#     return output
#
# print(longest_substring_with_atmost_k_char("eceba",2))     # "ece"
# print(longest_substring_with_atmost_k_char("ccaabbb",2))   # "aabbb"
# print(longest_substring_with_atmost_k_char("abcabcabc",2)) # "bca" or "abc"

# t = (1, 2, 3)
# print(id(t))
# # t[0] = 4  # This would raise a TypeError because tuples are immutable
# t = t + (4,)  # Creates a new tuple object
# print(id(t))

#
# from typing import List
# from collections import Counter
#
# def longest_subsequence_0_1(sequence: List[int]) -> List[int]:
#     if not sequence:
#         return [-1]
#     prefix_sum = 0
#     prefix_sum_counter = {0 : -1}
#     max_len = 0
#     res = 0
#     for i, num in enumerate(sequence):
#         prefix_sum += 1 if num == 1 else -1
#         if prefix_sum in prefix_sum_counter:
#             length = i - prefix_sum_counter[prefix_sum]
#             if max_len < length:
#                 max_len = length
#                 start = prefix_sum_counter[prefix_sum] + 1
#                 res = sequence[start:i+1]
#         else:
#             prefix_sum_counter[prefix_sum] = i
#     return max_len, res
#
# print(longest_subsequence_0_1([1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]))


# def most_common(nums: List[int], k: int) -> List[int]:
#     if not nums:
#         return [0]
#     return [num for num, _ in Counter(nums).most_common(k)]
# print(most_common([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5,5,5,5,5,5,7,7,7,7,7,7,3,3,3,2,2,2,2,],3))

#
# from typing import List
#
# def dailyTemperature(temperatures: List[int]) -> List[int]:
#     if not temperatures:
#         return [-1]
#     res = [0] * len(temperatures)
#     stack = []
#     for i, temp in enumerate(temperatures):
#         while stack and temp > temperatures[stack[-1]]:
#             prev_i = stack.pop()
#             res[prev_i] = i - prev_i
#         stack.append(i)
#     return res
#
#
# print(dailyTemperature([73,74,75,71,69,72,76,73]))


# # Python code demonstrate the working of
# # sorted() with lambda
#
# # Initializing list of dictionaries
# list = [{"name": "Nandini", "age": 20},
#        {"name": "Manjeet", "age": 20},
#        {"name": "Nikhil", "age": 19}]
#
# # using sorted and lambda to print list sorted
# # by age
# print("The list printed sorting by age: ")
#
# print(sorted(list, key=lambda i: i['age']))
#
#
#
# # using sorted and lambda to print list sorted
# # by both age and name. Notice that "Manjeet"
# # now comes before "Nandini"
# print("The list printed sorting by age and name: ")
# print(sorted(list, key=lambda i: (i['age'], i['name'])))
#
# print("\r")
#
# # using sorted and lambda to print list sorted
# # by age in descending order
# print("The list printed sorting by age in descending order: ")
# print(sorted(list, key=lambda i: -i['age'], reverse=True))


# array = [1,2,3,4,5,6,7,8,9]

# def max_sum_of_k(arr: List[int], k: int) -> int:
#     if not arr or k == 0:
#         return 0
#     temp_sum = sum(arr[:k])
#     max_sum = temp_sum
#     for i in range(1,len(arr)-k+1):
#         temp_sum = temp_sum + arr[i+k-1] - arr[i-1]
#         if temp_sum > max_sum:
#             max_sum = temp_sum
#             array = arr[i:i+k]
#     return max_sum, array
#
# print(max_sum_of_k([1,2,3,4,5,6,7,8,9,111,-98,1212,2212,0,12],3))

from typing import List

#
# def prefix_sum_to_k(arr: List[int], k: int):
#     if not arr:
#         return 0, []
#
#     prefix_sum = 0
#     seen = {0: -1}  # important: sum 0 is seen before index 0
#     max_len = 0
#     result = []
#
#     for i, num in enumerate(arr):
#         prefix_sum += num
#
#         if prefix_sum - k in seen:
#             length = i - seen[prefix_sum - k]
#             if length > max_len:
#                 max_len = length
#                 start = seen[prefix_sum - k] + 1
#                 result = arr[start:i + 1]
#
#         # Only store the **first** occurrence
#         if prefix_sum not in seen:
#             seen[prefix_sum] = i
#
#     return max_len, result


# def selection_sort(arr: List[int]) -> List[int]:
#     if not arr:
#         return []
#     for i in range(len(arr)):
#         current_index = i
#         for r in range(i+1,len(arr)):
#             if arr[r] < arr[current_index]:
#                 current_index = r
#         arr[i],arr[current_index] = arr[current_index],arr[i]
#     return arr
#
# print(selection_sort([12,4,24,121,1,34,11,1,2,4]))
#


# def three_sum(arr: List[int], target: int) -> List[int]:
#     if not arr or len(arr) < 3:
#         return []
#     sorted_arr = sorted(arr)
#     for i in range(len(sorted_arr)-2):
#         j = i + 1
#         k = len(arr) - 1
#         while j < k:
#             current_sum = arr[i] + arr[j] + arr[k]
#             if current_sum == target:
#                 return [i, j, k]
#             elif current_sum > target:
#                 k -= 1
#             elif current_sum  < target:
#                 j += 1
#     return []
#
# print(three_sum([12,2,4,45,6,7,88,3,9],100))



# def insertion_sort(arr: List[int]) -> List[int]:
#     if not arr:
#         return []
#     for i in range(len(arr)):
#         temp = arr[i]
#         r = i-1
#         while r >= 0 and temp < arr[r]:
#             arr[r+1] = arr[r]
#             r -= 1
#         arr[r+1] = temp
#     return arr
#
# print(insertion_sort([121,2,3,12,3,12,12,1,2,3,4,6,78,12]))

from typing import List, Tuple

# def bubble_sort(arr: List[int]) -> List[int]:
#     if not arr:
#         return arr
#     for i in range(len(arr)):
#         swapped = False
#         for j in range(len(arr)-1, i-1,-1):
#             if arr[j-1] > arr[j]:
#                 arr[j],arr[j-1] = arr[j-1],arr[j]
#                 swapped = True
#         if not swapped:
#             break
#     return arr
#
# print(bubble_sort([1212,2,331,3,312,312,21,1]))

# from typing import List, Tuple
#
# def merge_sort(arr: List[int]) -> List[int]:
#     if len(arr) <= 1:
#         return arr
#     left_arr, right_arr = split_arr(arr)
#     left_sorted = merge_sort(left_arr)
#     right_sorted = merge_sort(right_arr)
#     return merge_arr(left_sorted,right_sorted)
#
# def split_arr(arr: List[int]) -> Tuple[List[int], List[int]]:
#     mid = len(arr) // 2
#     left_arr = arr[:mid]
#     right_arr = arr[mid:]
#     return left_arr,right_arr
#
# def merge_arr(left: List[int], right: List[int]) -> List[int]:
#     i = j = 0
#     merged = []
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             merged.append(left[i])
#             i +=1
#         else:
#             merged.append(right[j])
#             j += 1
#     merged.extend(left[i:])
#     merged.extend(right[j:])
    return merged


print(merge_sort([12, 23123, 2, 33, 12, 2, 1, 45, 57, 8, 32312, 2223, 3]))