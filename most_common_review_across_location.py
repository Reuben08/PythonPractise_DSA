

from typing import List
from collections import Counter

class Reuben():
    def most_common_review(self, data: dict[str,List[str]] ) -> str:
        if not data:
            return ""
        comment_array = []
        for comment_city in data.values():
            for comment in set(comment_city):
                comment_array.append(comment)
        counter_comment = Counter(comment_array)
        sorted_counter = sorted(counter_comment.items(), key = lambda x: (-x[1],x[0]))
        return sorted_counter[0][0]

    def maximum_total_purchases(self, logs: List[dict[str,str,int]]) -> str:
        if not logs:
            return "null"
        amount_counter = defaultdict(int)
        for log in logs:
            user = log["user_id"]
            amount = log["amount"]
            amount_counter[user] += amount
        sorted_amount = sorted(amount_counter.items(), key = lambda x:(-x[1],x[0]))
        return sorted_amount[0][0]


arey = [12,23,23,1,2,4,4,-123,543]
arey.sort(reverse = True)
print(arey)
