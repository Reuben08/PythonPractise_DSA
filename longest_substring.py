# from typing import List, Dict
#
# class Reuben():
#     def longest_substring(self, s: str) -> int:
#         l = 0
#         Charset = set()
#         max_length = 0
#         for r in range(len(s)):
#             while s[r] in Charset:
#                 Charset.remove(s[l])
#                 l += 1
#             Charset.add(s[r])
#             max_length = max(max_length, r-l+1)
#         return max_length
#
#     def users_on_multiple_date(self, logs: List[Dict[str,str]]) -> List[str]:
#         if not logs:
#             return []
#         counter = defaultdict(set)
#         for log in logs:
#             user = log["user_id"]
#             date = log["date"]
#             counter[user].add(date)
#         result = []
#         for user in counter.keys():
#             if len(counter[user]) > 1:
#                 result.append(user)
#         return result
#
#     def group_actions_by_user(self, logs: List[Dict[str,str]])-> Dict[str,List[str]]:
#             if not logs:
#               return {}
#             final = defaultdict(List)
#             for log in logs:
#                 user = log[user_id]
#                 action = log[action]
#                 final[user].append(action)
#             return final
#
#     def group_unique_users(self, logs: List[Dict[str,str]]) -> Dict(str, Set[str]):
#             if not logs:
#                 return {}
#             result = defaultdict(set)
#             for log in logs:
#                 user = log["user_id"]
#                 timestamp = log["timestamp"]
#                 timestamp.split("T")[0]
#                 result[timestamp].add(user)
#             return result
#
#
#     def top_N_actions(self, logs: List[Dict[str,str]], n: int) -> List[str]:
#             if not logs:
#                 return ["null"]
#             action_dict = defaultdict(int)
#             for log in logs:
#                 action = log["action"]
#                 action_dict[action] += 1
#             sorted_array = sorted(action_dict.items(), key = lambda x:(-x[1],x[0]))
#             return sorted_array[:n][0]
#
#
#     def first_non_repeating(self, comments: List[str], banned:  List[str])-> str:
#             if not comments:
#                 return "null"
#             full_words = []
#             for comment in comments:
#                 clean_comment = re.sub(r'[^\w\s]','',comment.lower())
#                 full_words.extend(clean_comment.split())
#             final_dict = defaultdict(int)
#             for word in full_words:
#                 if word not in banned:
#                     final_dict[word] += 1
#             for word,freq in final_dict.items():
#                 if freq == 1:
#                     return word
#
#     def products_purchased_multiple_user(self, logs: List[Dict[str,str]]) -> List[str]:
#             if not logs:
#                 return ['null']
#             user_counter = defaultdict(set)
#             for log in logs:
#                 user = log["user_id"]
#                 product = log["product"]
#                 user_counter[product].add(user)
#             final_output = []
#             for product,freq in user_counter.items():
#                 if len(freq) > 1:
#                     final_output.append(product)
#
#     def date_with_highest_logins(self, logs: List[Dict[str,str]]) -> str:
#             if not logs:
#                 return "null"
#             login_counter = defaultdict(int)
#             for log in logs:
#                 timestamp = log["timestamp"]
#                 final_timestamp = timestamp.split("T")[0]
#                 activity = log["activity"]
#                 if activity == 'login':
#                     login_counter[final_timestamp] += 1
#             sorted_login = sorted(login_counter.items(), key = lambda x:(-x[0],x[1]))
#             return sorted_login[0][0]
#
#     def users_with_repeat_purchases(logs: List[Tuple[str, str]]) -> List[str]:
#             if not logs:
#                 return ["null"]
#             product_counter = defaultdict(list)
#             for user,product in logs:
#                 product_counter[user].append(product)
#             output_users = []
#             for user,product_list in product_counter.items():
#                 if len(product_list) > 1:
#                     output_users.append(user)
#             return output_users
#
#     def top_k_frequent_products(stream: List[str], k: int) -> List[str]:
#             if not stream:
#                 return [""]
#             stream_counter = Counter(stream)
#             output = []
#             for item,count in stream_counter.most_common(k):
#                 output.append(item)
#             return output
#     def largest_number(self, nums: List[int]) -> int:
#         if not nums:
#                 return 0
#             largest = nums[0]
#             for i in range(1,len(nums)-1):
#                 if nums[i] < nums[i+1]:
#                     largest = nums[i+1]
#             return largest
#     def second_largest(self, nums:List[int])->int:
#             if not nums:
#                 return 0
#             sorted_nums = nums.sort()
#             return sorted_nums[1]


logs = [
    {"user": "alice", "timestamp": "2025-05-03T14:22:35"},
    {"user": "bob", "timestamp": "2025-05-03T17:10:00"},
    {"user": "alice", "timestamp": "2025-05-04T08:00:00"}
]

from collections import defaultdict
from datetime import datetime

login_counter = defaultdict(int)

for log in logs:
    date_object = datetime.strptime(log["timestamp"],"%Y-%m-%dT%H:%M:%S")
    date_only = date_object.date()
    time_only = date_object.time()
    print(date_only)
    print(time_only)


for i in range(6):
    if i == 3:
        continue
    print(i)
struing = "skdjfhksdhTfkhdskTfhskdfj"
print(struing.find("T",1))