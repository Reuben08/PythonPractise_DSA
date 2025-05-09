from typing import List, Tuple
from collections import Counter

class Reuben():
    def common_purchased_product(self, user_transactions: List[Tuple[int, str]]) -> str:
        user_array = [product for _,product in user_transactions]
        user_counter = Counter(user_array)
        return user_counter.most_common(1)[0][0]
    def nth_smallest_value(self, data: dict[str, str], n: int)-> str:
        if n == 0 or n > len(data):
            return "null"
        sorted_array = sorted(data.items(), key = lambda x:(x[1],x[0]))
        return sorted_array[n-1][0]
    def most_active_user_from_logs(self, logs: List[str]) -> str:
        if not logs:
            return "mull"
        user_array = []
        for string in logs:
            user_array.append(string.split()[0])
        user_counter = Counter(user_array)
        return user_counter.most_common(1)[0]

object = Reuben()
print(object.common_purchased_product([
    (101, "Laptop"),
    (202, "Reuben"),
    (101, "Reuben"),
    (303, "Reuben"),
    (202, "Reuben"),
    (101, "Reuben"),
    (404, "Tablet"),
    (303, "Tablet"),
    (303, "Laptop")
]))
data = {
    "laptop": 999,
    "smartphone": 999,
    "smart_tv": 500,
    "smart_watch": 300,
    "smart_home": 9999999
}
print(Reuben().nth_smallest_value(data, 2))  # ✅ "smart_tv"
