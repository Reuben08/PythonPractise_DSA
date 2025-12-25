

from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    if not nums:
        return [0,0]
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i

print(two_sum([2,5,7,9],7))