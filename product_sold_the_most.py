from typing import List, Dict
from collections import defaultdict


class Reuben:
    def most_sold_product(self, sales_data: List[Dict[str, int]]) -> str:
        product_counter = defaultdict(int)
        for sale in sales_data:
            Product = sale["product"]
            Quantity = sale["quantity"]
            product_counter[Product] += Quantity
        sorted_product = sorted(product_counter.items(), key= lambda x: -x[1])
        return sorted_product[:1]


# ✅ Test Cases
obj = Reuben()
sales_data = [
    {"product": "Laptop", "quantity": 5},
    {"product": "Phone", "quantity": 10},
    {"product": "Tablet", "quantity": 7},
    {"product": "Laptop", "quantity": 8},
    {"product": "Phone", "quantity": 3},
    {"product": "Phone", "quantity": 3},
    {"product": "Phone", "quantity": 3},
    {"product": "Phone", "quantity": 3},
    {"product": "Phone", "quantity": 3}
]

print(obj.most_sold_product(sales_data))
