from collections import defaultdict, Counter
from typing import List, Dict

# class Reuben():
#     def first_banned_free_word(self, comments: List[str], stop_words: List[str]) -> str:
#         if not comments:
#             return ""
#         array = []
#         for string in comments:
#             clean_string = re.sub(r'[^\w\s]' ,'' ,string.lower())
#             array.extend(clean_string.split())
#             final_array = []
#         for word_final in array:
#             if word_final not in stop_words:
#                 final_array.append(word_final)
#                 counter_final = Counter(final_array)
#         return counter_final.most_common(1)[0][0]

    def most_frequent_product_by_user(self, logs: List[Dict[str, str]]) -> Dict[str, str]:
        if not logs:
            return {""}
        product_counter = defaultdict(Counter)
        for log in logs:
            user = log["user"]
            product = log["product"]
            product_counter[user][product] += 1
        result = {}
        print(product_counter.items())
        print(list(product_counter[user].elements()))

        for user,counter in product_counter.items():
            max_product = sorted(counter.items(), key=lambda x:(-x[1],x[0]))
            result[user] = max_product[0][0]
        return result







    # def list_intersection(self, list1: List[str], list2: List[str]) -> List[str]:
    #     if not list1:
    #         return list2
    #     if not list2:
    #         return list1
    #     array = []
    #     for word1 in list1:
    #         if word1 not in list2:
    #             array.append(word1)
    #     for word2 in list2:
    #         if word2 not in list1:
    #             array.append(word2)
    #     return array


logs = [
    {"user": "alice", "product": "book"},
    {"user": "alice", "product": "pen"},
    {"user": "alice", "product": "book"},
    {"user": "bob", "product": "pen"},
    {"user": "bob", "product": "pencil"},
    {"user": "bob", "product": "pen"},
]

r = Reuben()
print(r.most_frequent_product_by_user(logs))
