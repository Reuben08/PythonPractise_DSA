



from typing import List
from collections import Counter
import heapq

class Reuben:
    def top_k_elements(self, stream: List[int], K: int) -> List[int]:
        # Step 1: Count occurrences of each number
        stream_dict = Counter(stream)

        # Step 2: Get top K frequencies
        max_freq = heapq.nlargest(K, stream_dict.values())

        # Step 3: Extract numbers with top K frequencies, sorted by (frequency, number)
        sorted_items = sorted(stream_dict.items(), key=lambda x: (-x[1], -x[0]))

        # Step 4: Return top K numbers
        return [num for num, freq in sorted_items[:K]]

# ✅ Test Case
obj = Reuben()
stream = [4, 1, 2, 2, 3, 1, 1, 4, 4, 4, 5, 6, 6, 6, 6]
k = 3
print(obj.top_k_elements(stream, k))  # Expected Output: [6, 4, 1]


# # Creation of a Counter Class object using
# # string as an iterable data container
# x = Counter("geeksforgeeks")
# print(x)
# # printing the elements of counter object
# for i in x.elements():
#     print ( i, end = " ")



