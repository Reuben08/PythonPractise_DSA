from typing import List, Tuple
from collections import Counter, defaultdict

class Reuben():
    def top_spender(self, transactions: List[Tuple], K: int) -> List[Tuple]:
        customer_spending = Counter()
        for (customer,transaction) in transactions:
            customer_spending[customer] += transaction
        sorted_transaction = sorted(customer_spending.items(), key = lambda x:x[1], reverse = True)
        return sorted_transaction[:K]

obj = Reuben()
print(obj.top_spender([
    (101, 250),
    (202, 300),
    (101, 150),
    (303, 500),
    (202, 400),
    (404, 50),
    (101, 100),
    (303, 200)
],2))
