
from typing import List
from collections import Counter

class Reuben():
    def find_uncommon_elements(self, list_1: List[int], list_2: List[int]) -> list:
        set_1 = set(list_1)
        set_2 = set(list_2)
        return list((set_1 - set_2 | set_2 - set_1))

    def merge_list(self, data: Dict[str, List[str]]) -> List[str]:
        if not data:
            return []
        list1 = data["A"]
        list2 = data["B"]
        result = []
        for a, b in zip(list1, list2):
            result.append(a+b)
        return result
    def

object = Reuben()
print(object.find_uncommon_elements([1, 2, 3, 4, 5,90,871234],[1,2,3,4,5,18237]))


set_reuben = {1:100, 5:101, 7:101, 9:909, 3:800}
print(max(set_reuben.values()))



