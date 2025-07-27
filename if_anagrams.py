
from collections import defaultdict
class Reuben():
    def if_anagrams(self, str_1: str, str_2: str) -> bool:
        if not str_1 or not str_2:
            return False
        str_count = defaultdict(int)
        for string in str_1:
            str_count[string] += 1
        for string in str_2:
            str_count[string] -= 1
        for string, value in str_count.items():
            if value != 0:
                return False
        return True





object = Reuben()
print(object.if_anagrams("ccddaaaa","aaccdd"))
