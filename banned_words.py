import re
from typing import List
from collections import Counter

class Reuben:
    def ignore_banned_words(self, para: str, banned: List[str]) -> str:
        # Convert to lowercase and remove punctuation
        para_lower = re.sub(r'[^\w\s]', '', para.lower())

        # Split into words (handles multiple spaces properly)
        para_lower_array = para_lower.split()

        # Remove banned words using a for loop
        filtered_words = []  # New list to store valid words
        for word in para_lower_array:
            if word not in banned:
                filtered_words.append(word)  # Append only non-banned words

        # Count occurrences of the remaining words
        count = Counter(filtered_words)

        # Return the most common non-banned word
        return count.most_common(1)[0][0] if count else ""

    def most_purchased_product(self, logs: List[Dict[str, str]]) -> str:

        if not logs:
            return "null"

        product_counter = defaultdict(int)
        for log in logs:
            product = log["product"]
            product_counter[product] += 1
        sorted_count = sorted(product_counter.items(), key = lambda x:(-x[1],x[0]))
        return sorted_count[0][0]

    def count_unique_elements_in_window(self, nums: List[int], k: int) -> List[int]:
        if not nums or len(nums) < k:
            return [0]
        final_array = []
        for i in range(len(nums)-k+1):
            sub_array = nums[i:i+k]
            count = len(set(sub_array))
            final_array.append(count)
        return final_array

    def max_spending_user(self, logs: List[Dict[str, int]]) -> str:
        if not logs:
            return "null"
        amount_counter = defaultdict(int)
        for log in logs:
            user = log["user_id"]
            amount = log["amount"]
            amount_counter[user] += amount
        sorted_amount = sorted(amount_counter.items(), key = lamnda x:(-x[1],x[0]))
        return sorted_amount[0][0]

    def second_largest_num(self, inputList: List[int])->int:
        if not input:
            return float('-inf')
    max_num = max(inputList



# ✅ Test Case
obj = Reuben()
paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
banned = ["hit"]

print(obj.ignore_banned_words(paragraph, banned))  # Expected Output: "ball"
