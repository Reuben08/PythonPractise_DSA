


from typing import List
class Reuben():
    def merge_sorted_array(self,nums_1: List[int], nums_2: List[int]) -> List[int]:
        output = []
        for nums in nums_1:
            output.append(nums)
        for nums in nums_2:
            output.append(nums)
        return output

obj = Reuben()
print(obj.merge_sorted_array([1, 3, 5, 7], [2, 4, 6, 8]))
# Expected Output: [1, 2, 3, 4, 5, 6, 7, 8]
