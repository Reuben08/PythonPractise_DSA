"""
CS 6603 – AI, Ethics, and Society
Assignment #1 – Facebook/Instagram Advertiser Sampling

This script extracts distinct advertisers from the Meta data file
'advertisers_using_your_activity_or_information.json' and randomly samples
120 advertisers to be analyzed in the assignment.

Author: Reuben Haruray
GT Username: rharuray3
"""

import json
import random

# Step 1: Load the JSON data from Instagram
with open('/Users/reubenharuray/Downloads/ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.json', 'r') as file:
    data = json.load(file)

# Step 2: Extract advertiser names from the list
advertisers_data = data.get('ig_custom_audiences_all_types', [])
advertisers = [entry['advertiser_name'] for entry in advertisers_data if 'advertiser_name' in entry]

# Step 3: Get distinct advertisers
unique_advertisers = list(set(advertisers))
total_unique = len(unique_advertisers)

print(f"Total unique advertisers found: {total_unique}")

# Step 4: Sample 120 advertisers
sample_size = min(120, total_unique)
sampled_advertisers = random.sample(unique_advertisers, sample_size)

print(f"\nRandom sample of {sample_size} advertisers:\n")
for adv in sampled_advertisers[:120]:
    print(f" - {adv}")