


from typing import List, Tuple
from collections import defaultdict
from datetime import datetime

class Reuben:
    def user_session_analysis(self, logs: List[Tuple[str, str, str]]) -> dict:
        user_first_login = {}

        for user, action, timestamp in logs:
            timeobj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            if user not in user_first_login:
                user_first_login[user] = (timeobj, action)
            else:
                current_time, _ = user_first_login[user]
                if timeobj < current_time:
                    user_first_login[user] = (timeobj, action)

        return {user: timeobj for user, (timeobj, action) in user_first_login.items()}

    def most_active_user(self, logs: List[str]) -> str:
        if not logs:
            return ""
        user_count = []
        for log in logs:
            user_count.append(log.split()[0])
        count_user = Counter(user_count)
        return count_user.most_common(1)[0][0]

    def unique_elements_sliding_window(self, nums: List[str], k: int) -> List[int]:
        if not nums or k > len(nums):
            return []
        sub_array = []
        for i in range(len(nums)-k+1):
            temp_array = nums[i:i+k]
            count = len(set(temp_array))
            sub_array.append(count)
        return sub_array

    def min_subarray_len(self, target: int, nums: List[int]) -> int:
        if not nums:
            return 0
        seen = {}
        for i,num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return len[seen[diff],i]
            else:
                seen[num] = i
            return 0

    def max_unique_items(self, prices: List[int], budget: int) -> int:
        if not prices:
            return 0
        sum = 0
        for i in range(len(prices)):
            sum += sum(prices[i:i+1])
            if sum >= budget:
                continue
        return i+1



object = Reuben()
print(object.user_session_analysis([
    ("1001", "login", "2024-02-15 08:00:00"),
    ("1001", "click", "2024-02-15 08:10:00"),
    ("1001", "view", "2024-02-15 08:20:00"),
    ("1001", "logout", "2024-02-15 08:30:00"),

    ("2002", "login", "2024-02-15 09:00:00"),
    ("2002", "click", "2024-02-15 09:10:00"),
    ("2002", "view", "2024-02-15 09:20:00"),
    ("2002", "click", "2024-02-15 09:25:00")]))
# reuben = [1,2,3,4,5,6,7]
# print(reuben[0:4])
# for i in range(3):
#     print(i)
string = "1241234"
digits = list(string)
print(digits)



