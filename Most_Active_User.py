from typing import List, Tuple
from collections import Counter, defaultdict

class Reuben():
    def most_active_user(self, logs: List[str]) -> str:
        if not logs:
            return ""
        log_array = []
        for log in logs:
            log_array.append(log.split()[0])
        activity_counter = Counter(log_array)
        sorted_counter = sorted(activity_counter.items(), key = lambda x:(-x[1],x[0]))
        return sorted_counter[0][0]

    def

obj = Reuben()
print(obj.most_active_user([
    "1234 login 2024-02-14 12:30:45",
    "5678 click 2024-02-14 12:31:10",
    "1234 logout 2024-02-14 12:32:05",
    "5678 login 2024-02-14 12:33:15",
    "1234 click 2024-02-14 12:34:10",
    "5678 logout 2024-02-14 12:35:30",
    "5678 click 2024-02-14 12:36:00",
    "5678 click 2024-02-14 12:37:15"
]))

string = "1234 login 2024-02-14 12:30:-4-5"
print(string.split("-",1))