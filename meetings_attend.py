
from typing import List
class Reuben():
    def can_attend_meeting(self, input: List[List[int]]) -> bool:
        if not input:
            return False
        sorted_input = sorted(input)
        for i in range(len(sorted_input)):
            if sorted_input[i][1] > sorted_input[i+1][0]:
                return False
            else:
                return True


object = Reuben()
print(object.can_attend_meeting([[1,5],[2,4]]))



