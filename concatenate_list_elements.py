from typing import List, Tuple

class Reuben:
    def concatenate_list_elements(self, strings: List[List[str]]) -> List[str]:
        output = []
        for lists in strings:
            for elements in lists:
                output.append(elements)
        return output
    def reuben_window(self, nums: List[int], k: int)-> int:
        if not nums or k == 0:
            return 0
        for i in range(len(nums)-k+1):


obj = Reuben()
print(obj.concatenate_list_elements([[1,2,3,4,5], [2,3,4,5,6,7,8]]))



