
from collections import Counter

class Reuben():
    # def max_occurence_location(self, location: dict) -> str:
    #     location_counter = Counter()
    #     for cities in location.values():
    #         for city in cities:
    #             location_counter[city] += 1
    #     return location_counter.most_common()
    #
    # def most_purchased_product(self, logs: List[dict[str,str]]) -> str:
    #     if not logs:
    #         return "null"
    #     product_counter = defaultdict(int)
    #     for log in logs:
    #         product = log["product"]
    #         product_counter[product] += 1
    #     sorted_list = sorted(product_counter.items(), key = lambda x:(-x[1],x[0]))
    #     return sorted_list[0][0]

    def largest_odd_rearranged(self, num_str: int) -> int:
        if not num_str:
            return 'null'
        sorted_string = sorted(str(num_str), reverse = True)
        if int("".join(sorted_string)) % 2 == 1:
            return "".join(sorted_string)
        else:
            return -1


obj = Reuben()
print(obj.largest_odd_rearranged("1234"))  # Output: "4312" or similar valid highest
print(obj.largest_odd_rearranged("2468"))  # Output: "-1"


