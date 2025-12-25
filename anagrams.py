from collections import Counter, defaultdict
from typing import List, Dict
class Reuben():
    def anagrams_finder(self, words: List[str]) -> List[List[str]]:
        anagram_groups = defaultdict(list)
        for word in words:
            sorted_word = "".join(sorted(word))
            anagram_groups[sorted_word].append(word)
        return list(anagram_groups.values())
    def anagram_counter(self, words: List[str]) -> List[List[str]]:
        if not words:
            return ['null']
        anagram_dict = defaultdict(list)
        for word in words:
            sorted_word = sorted(word)
            anagram = "".join(sorted_word)
            anagram_dict[anagram].append(word)
        return list(anagram_dict.values())
    def common_review(self, reviews: Dict[str,list[str]])-> str:
        if not reviews:
            return "null"
        unique_comments = []
        for location in reviews.keys():
            unique_comments.extend(set(reviews[location]))
        comment_counter = Counter(unique_comments)
        return comment_counter.most_common(1)[0][0]

    def common_review_GPT(self, reviews: Dict[str, List[str]]) -> str:
        if not reviews:
            return "null"

        review_count = defaultdict(int)

        for location in reviews:
            for review in set(reviews[location]):
                review_count[review] += 1

        # Sort to break ties lexicographically
        sorted_reviews = sorted(review_count.items(), key=lambda x: (-x[1], x[0]))
        return sorted_reviews[0][0]

    def remove_stop_words(self, comments: List[str], stop_words: List[str])->str:
        if not comments:
            return "null"
        full_list = []
        for comment in comments:
            clean_comment = re.sub(r'[^\w\s'],'', comment.lower())
            full_list.extend(clean_comment.split())
        final_list
        for word in full_list:
            if word not in stop_wo
    def category_maximum_3(self, category_points: List[Tuple[str,int]])-> int:
        if not category_points:
            return 0
        category_counter = defauldict(list)
        for category,points in category_points:
            category_counter[category].append(points)
        max_list = []
        for category, list in category_counter.items():
            max_per_category = max(category_counter[category])
            max_list.append(max_per_category)
        sorted_max = sorted(max_list, reverse = True)
        return sum(sorted_max[:3])

from typing import List, Tuple

    def validate_checkout(logs: List[Tuple[int, bool]]) -> bool:
        if not logs:
            return False
        is_checkout_out = set()
        for book, is_checked_out in logs:
            if is_checkout_out:
                if book in is_checkout_out:
                    return False
                is_checked_out.add(book)
            else:
                if book not in is_checkout_out:
                    return False
                is_checked_out.remove(book)
        return True





