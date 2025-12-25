import statistics as stat
from typing import List
class Reuben():
    def extract_odd_then_big(self, I: int) -> int:
        array = []
        for i in str(I):
            if int(i) % 2 == 1:
                array.append(i)
        array.sort(reverse = True)
        return int("".join(array))

    def data_merge(self, data: dict[str,List[str]]) -> List[str]:
        if not data:
            return null
        list1 = data["A"]
        list2 = data["B"]
        array = []
        for a,b in zip(list1, list2):
            array.append(a+b)
        return array
    def most_freq(self, logs: List[str], stop_words : List[str])-> str:
        if not logs:
            return ""
        full_log = []
        for log in logs:
            clean_log = re.sub(r'[^/w/d]','',log.lower())
            full_log.extend(clean_log.split())
        final_log = []
        for word in full_log:
            if word not in stop_words:
                final_log.append(word)
        counter_final = Counter(final_log)
        return counter_final.most_common(1)[0][0]

    def most_consecutive_years(self, years: List[int]) -> int:
        if not years:
            return 0
        workshop_counter = Counter(years)
        sorted_years = list(sorted(workshop_counter.keys()))
        max_count = 0
        for i in range(len(sorted_years)-1):
            count = workshop_counter[sorted_years[i]] + workshop_counter[sorted_years[i+1]]
            max_count = max(count,max_count)
        return max_count

    def anagram_counter(self, words: List[str]) -> List[List[str]]:
        if not words:
            return ['null']
        anagram_dict = defaultdict(List[str])
        for word in words:
            sorted_word = sorted(word)
            anagram = "".join(sorted_word)
            anagram_dict[anagram].append(word)
        return list(anagram_dict.values())








object = Reuben()
print(object.extract_odd_then_big(54321))
print(object.data_merge({"A": ["x1","x2","x3"], "B": ["y1","y2","y3"]}))
for i in range(8):
    print(i)

for i in range(7):
    print(i)
print((''.join(['we','asd','123'])))
