from typing import List


class Reuben():
    def top_K_elements(self, nums: List[int], k: int) -> List[int]:
        freq = {}
        for num in nums:
            if num in freq:
                freq[num] += 1
            else:
                freq[num] = 1
        sorted_freq = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
        return sorted_freq[:k]

object = Reuben()
print(object.top_K_elements([1,1,1,1,2,3,4,5], 2))