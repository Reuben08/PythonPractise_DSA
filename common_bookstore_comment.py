


from typing import List
from collections import Counter

class Reuben():
    def common_hashtag(self, Diction: dict) -> str:
        if not Diction:
            return ""
        comment_counter = Counter()
        for rest in Diction.values():
            for comments in set(rest):
                comment_counter[comments] += 1
        return comment_counter.most_common(1)[0][0]

    def top_review_word(self, reviews: dict[str, List[str]], banned: List[str]) -> str:
        if not reviews:
            return 'null'
        all_words = []
        for review in reviews.values():
            for string in set(review):
                clean_string = re.sub(r'[\w\s]','',string.lower())
                all_words.extend(clean_string.split())
        final_list = []
        for word in all_words:
            if word not in banned:
                final_list.append(word)
        counter_word = Counter(final_list)
        return counter_word.most_common(1)[0][0]

    def user_product_counts(self, logs: List[Tuple[str, str]], threshold: int) -> Dict[str, int]:
        if not logs:
            return {}
        product_counter = defaultdict(set)
        for log in logs:
            for user,product in log:
                product_counter[user].add(product)
        final_out = defaultdict(int)
        for user,product in product_counter.items():
            if len(product_counter[user]) > threshold:
                final_out[user] += 1
        return final_out

    def frequent_product_buyers(logs: List[Tuple[str, str]]) -> Dict[str, int]:
        if not logs:
            return {}
        user_counter = defaultdict(Counter)
        for user, product in logs:
            user_counter[product][user] += 1
        user_num_counter = defaultdict(int)
        for product, user in user_counter.items():
            if user.values() > 1:
                user_num_counter[product] += 1
        return user_num_counter

    def user_repeat_score(logs: List[Tuple[str, str]]) -> Dict[str, int]:
        if not logs:
            return {}
        product_counter = defaultdict(Counter)
        for user, product in logs:
            product_counter[user][product] += 1
        final_users = defaultdict(int)
        for user,products in product_counter.items():
            if product.values() > 1:
                final_users[user] += 1
        return final_users

    def most_active_user(self, logs: List[str]) -> str:
        if not logs:
            return ""
        user_array = []
        for log in logs:
            user_array.append(log.split()[0])
        user_counter = Counter(user_array)
        user_sorted =sorted(user_counter.items(), key = lambda x:[-x[1],x[0]])
        return user_sorted[0][0]






obj = Reuben()
hashtags = {
    "influencer_1": ["#fitness", "#healthy", "#gym", "#fitness"],
    "influencer_2": ["#yoga", "#fitness", "#meditation", "#healthy"],
    "influencer_3": ["#fitness", "#gym", "#meditation", "#gym"]
}

print(obj.common_hashtag(hashtags))


