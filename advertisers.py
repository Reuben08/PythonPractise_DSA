


import json
import random
from collections import defaultdict

# Step 1: Load Advertisers
with open('/Users/reubenharuray/Downloads/ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.json', 'r') as file:
    data = json.load(file)

all_advertisers = list(set([entry['advertiser_name'] for entry in data['ig_custom_audiences_all_types'] if 'advertiser_name' in entry]))
print(f"✅ Total unique advertisers: {len(all_advertisers)}")

# Step 2: Random Sample of 200
sampled_advertisers = random.sample(all_advertisers, 200)

# Step 3: Define Category Rules
category_keywords = {
    'Finance': ['bank', 'credit', 'loan', 'fund', 'finance', 'invest', 'capital'],
    'Education': ['college', 'school', 'academy', 'edu', 'course', 'university'],
    'Retail': ['shop', 'store', 'brand', 'fashion', 'retail', 'wear', 'style'],
    'Technology': ['tech', 'digital', 'software', 'app', 'cloud', 'platform'],
    'Lifestyle': ['media', 'blog', 'health', 'life', 'food', 'fitness', 'travel']
}

def classify_category(name):
    name_lower = name.lower()
    for category, keywords in category_keywords.items():
        if any(kw in name_lower for kw in keywords):
            return category
    return 'Other Category'

# Step 4: Assign Category & Relevance
def assign_relevance():
    r = random.random()
    if r < 0.3:
        return 'Yes'
    elif r < 0.8:
        return 'No'
    else:
        return 'U Got To Be Kidding'

category_relevance_counts = defaultdict(lambda: defaultdict(int))
category_totals = defaultdict(int)

for adv in sampled_advertisers:
    category = classify_category(adv)
    relevance = assign_relevance()
    category_relevance_counts[category][relevance] += 1
    category_totals[category] += 1

# Step 5: Print Correct Sankey Input
print("\n📊 SankeyMATIC Input — CORRECT FORMAT:")
# From FB Advertisers to each actual category
for category, total in category_totals.items():
    print(f"FB Advertisers [{total}] {category}")

# From each category to each relevance bucket
for category, relevance_counts in category_relevance_counts.items():
    for relevance, count in relevance_counts.items():
        print(f"{category} [{count}] {relevance}")

import json
import random
from collections import defaultdict

# --- Load advertiser data ---


advertisers = list(set([entry['advertiser_name'] for entry in data['ig_custom_audiences_all_types'] if 'advertiser_name' in entry]))

# --- Sample 200 advertisers ---
sampled_advertisers = random.sample(advertisers, 200)

# --- Regulated domain keywords ---
regulated_domains = {
    'Credit': ['credit', 'bank', 'loan', 'fund', 'finance', 'capital', 'lender'],
    'Education': ['college', 'school', 'academy', 'university', 'edu', 'training', 'learning'],
    'Employment': ['career', 'job', 'employment', 'recruit', 'staffing', 'hiring'],
    'Housing & Public Accommodation': ['property', 'realty', 'homes', 'housing', 'apartment', 'builder', 'estate']
}

# --- Match advertisers to domains ---
domain_matches = defaultdict(list)

for advertiser in sampled_advertisers:
    name = advertiser.lower()
    for domain, keywords in regulated_domains.items():
        if any(kw in name for kw in keywords):
            domain_matches[domain].append(advertiser)
            break  # One advertiser per domain max

# --- Display results ---
print("\n📊 Regulated Domain Information Table")
print(f"{'Regulated Domain':<35} {'Number of Items':<18} Advertiser Sample")
print("-" * 80)
for domain in ['Credit', 'Education', 'Employment', 'Housing & Public Accommodation']:
    advertisers_in_domain = domain_matches.get(domain, [])
    count = len(advertisers_in_domain)
    sample = ', '.join(advertisers_in_domain[:3]) if count else '—'
    print(f"{domain:<35} {str(count):<18} {sample}")