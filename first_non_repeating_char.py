
import re
from collections import Counter
class Reuben():
    def first_non_repeating_char(self, s: str) -> str:
        letter_counter = Counter(s)
        for char in s:
            if letter_counter[char] == 1:
                return char
        return "null"

    def most_frequent_word(self, comments: List[str], stop_words: List[str]) -> str:
        if not comments:
            return ""
        all_words = []
        for comment in comments:
            clean_comment = re.sub('r[^\w\s]','',comment.lower())
            all_words.extend(clean_comment.split())
        final_array = []
        for word in all_words:
            if word not in stop_words:
                final_array.append(word)
        counter_words = Counter(final_array)
        return counter_words.most_common(1)[0][0]

    def most_common_review(reviews: Dict[str, List[str]]) -> str:
        if not reviews:
            return ""
        word_list = []
        for city, reviews in reviews.items():
            for review in set(reviews):
                word_list.append(review)
        word_counter = Counter(word_list)
        return word_counter.most_common(1)[0][0]

    def common_words(comments: List[List[str]]) -> List[str]:
        if not comments:
            return [""]
        common_words = []
        for i in range(len(comments)):
            list_1 = comments[i] | comment_words
        return sorted(list_1)

    def most_purchased_per_user(logs: List[Tuple[str, str]]) -> Dict[str, str]:
        if not logs:
            return {"null","null"}
        product_counter = defaultdict(Counter)
        for user,product in logs:
            product_counter[user][product] += 1
        result = defaultdict(str)
        for user,product_list in product_counter.items():
            max_product = product_list.most_common(1)[0][0]
            result[user] = max_product
        return result





object = Reuben()
print(object.first_non_repeating_char("aabbcdc"))


string = "ksjdhf ksdjhf  hdsfihi khsdfhidhf ihfi hifhkhfkhskdf hdfihdkf ksf ;iuqosk h; dfiohwdif d;kshfihdsf"
clean_string = re.sub(r'[^\w\s]', '',string.lower())
print(clean_string)
print(string.split())