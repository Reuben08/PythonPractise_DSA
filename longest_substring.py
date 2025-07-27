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
#     def group_actions_by_user(self, logs: List[Dict[str,str]])-> Dict[str,List[str]]:
#         if not logs:
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
#             return 0
#         largest = nums[0]
#         for i in range(1,len(nums)-1):
#             if nums[i] < nums[i+1]:
#                 largest = nums[i+1]
#         return largest
#    def top_k_active_users(logs: List[Tuple[str, str, str]], k: int) -> List[str]:
#        if not logs:
#            return [""]
#        user_counter = Counter()
#        for user,_,_ in logs:
#            user_counter[user] += 1
#        sorted_user_counter = sorted(user_counter.items(), key = lambda x: (-x[1],x[0]))
#        return sorted_user_counter[:k]
#
#
# def top_k_purchase_users_jan_2023(logs: List[Tuple[str, str, str]], k: int) -> List[str]:
#     if not logs:
#         return [""]
#     user_action_counter = defaultdict(int)
#     for user, action, timestamp in logs:
#         timestamp_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
#         if action == 'purchase' and datetime.month(timestamp_object) == '01' and datetime.year(timestamp_object) == '2023':
#             user_action_counter[user] += 1
#     sorted_array = sorted(user_action_counter.items(), key = lambda x:(-x[1],x[0]))
#     return sorted_array[:k]
#
# def max_sum_subarray(nums: List[int], k: int) -> int:
#     if not nums or len(nums) < k:
#         return 0
#     window_sum = sum(nums[:k])
#     total_sum = window_sum
#
#     for i in range(k,len(nums)):
#         interim_sum += nums[k] - nums[i-k]
#         total_sum = max(total_sum, interim_sum)
#     return total_sum
#
# def length_of_longest_substring(s: str) -> int:
#     if not s:
#         return 0
#     charset = set()
#     l = 0
#     max_len = 0
#
#     for r in range(len(s)):
#         while s[r] in charset:
#             charset.remove(s[l])
#             l += 1
#         charset.add(s[r])
#         max_len = max(max_len, r - l + 1)
#
#     return max_len
#
# def find_common_words(comments: List[str]) -> List[str]:
#     if not comments:
#         return [""]
#     word_counter = defaultdict(int)
#     for comment in comments:
#         clean_comment = re.sub(r'[^\w\s]','',comment.lower())
#         clean_split = clean_comment.split()
#         for word in set(clean_split):
#             word_counter[word] += 1
#     final_output = []
#     for word, freq in word_counter.items():
#         if freq > 1:
#             final_output.append(word)
#     return final_output
#
# def daily_top_products(logs: List[Tuple[str, str, str]]) -> Dict[str, str]:
#     if not logs:
#         return {}
#     product_counter_per_date = defaultdict(Counter)
#     for user, prod, timestamp in logs:
#         date_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
#         date_final = date_time.date
#         product_counter_per_date[date_final][prod] += 1
#     final_out = {}
#     for date_purchased, prod_counter in product_counter_per_date.items():
#         final_out[date_purchased] = prod_counter.most_common(1)[0][0]
#     return final_out

# Re-import libraries after code execution state reset
import pandas as pd

# Redefine loan parameters
P = 62152.07
annual_rate = 0.0839
biweekly_rate = annual_rate / 26
biweekly_payment = 452.06979270654534  # As previously calculated
biweekly_periods = 7 * 26  # 182 payments

# Re-initialize values
starting_balance = 53247.72
target_balance = 44000
current_balance = starting_balance
interest_paid = 0
payments_count = 0
schedule_to_target = []

# Calculate payments from 37th onwards until balance hits or drops below 44,000
while current_balance > target_balance and payments_count < (biweekly_periods - 36):
    interest = current_balance * biweekly_rate
    principal_payment = biweekly_payment - interest
    current_balance -= principal_payment
    interest_paid += interest
    payments_count += 1
    print(f" Payment count:{payments_count}, Interest Paid: {interest_paid}, Principle deducted is:{(452.7*payments_count)-interest_paid}, Current balance: {current_balance}")
    schedule_to_target.append({
        "Payment Number": 36 + payments_count,
        "Payment Amount": round(biweekly_payment, 2),
        "Principal Paid": round(principal_payment, 2),
        "Interest Paid": round(interest, 2),
        "Remaining Balance": round(current_balance, 2)
    })



