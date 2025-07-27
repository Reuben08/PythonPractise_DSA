import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load the dataset
column_names = [
    "checking_account", "duration", "credit_history", "purpose", "credit_amount",
    "savings_account", "employment_since", "installment_rate", "personal_status_sex",
    "other_debtors", "residence_since", "property", "age", "other_installment_plans",
    "housing", "existing_credits", "job", "dependents", "telephone", "foreign_worker", "class"
]

df = pd.read_csv("/Users/reubenharuray/Downloads/statlog+german+credit+data/german.data-numeric", sep='\s+', header=None, names=column_names)

# Step 2: Define weights and selected features
features_with_weights = {
    "checking_account": 1.3,
    "duration": 1.0,
    "credit_amount": 1.5,
    "savings_account": 1.3,
    "employment_since": 1.2,
    "installment_rate": 1.0,
    "existing_credits": 1.0
}
selected_features = list(features_with_weights.keys())

# Step 3: Normalize and compute creditworthiness score
X = df[selected_features]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=selected_features)

weights_array = np.array([features_with_weights[f] for f in selected_features])
weighted_scores = X_scaled_df.mul(weights_array).sum(axis=1) / weights_array.sum()
df['creditworthiness_score'] = weighted_scores * 100

# Step 4: Balance the dataset (equal Good/Bad classes)
df_majority = df[df["class"] == 1]
df_minority = df[df["class"] == 2]
df_majority_downsampled = df_majority.sample(n=len(df_minority), random_state=42)
df_balanced = pd.concat([df_majority_downsampled, df_minority]).reset_index(drop=True)

# Recalculate the creditworthiness_score for df_balanced
X_bal = df_balanced[selected_features]
X_bal_scaled = scaler.transform(X_bal)
X_bal_scaled_df = pd.DataFrame(X_bal_scaled, columns=selected_features)

weights_array = np.array([features_with_weights[f] for f in selected_features])
df_balanced['creditworthiness_score'] = X_bal_scaled_df.mul(weights_array).sum(axis=1) / weights_array.sum() * 100

# Reassign age group
age_median = df_balanced['age'].median()
df_balanced['age_group'] = df_balanced['age'].apply(lambda x: 'Privileged' if x <= age_median else 'Unprivileged')

# Split into groups AFTER scores are recalculated
df_privileged = df_balanced[df_balanced['age_group'] == 'Privileged']
df_unprivileged = df_balanced[df_balanced['age_group'] == 'Unprivileged']

# Sanity check: print NaN count
print("NaNs in creditworthiness_score:")
print(df_balanced['creditworthiness_score'].isna().value_counts())

# Plot histograms
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

axes[0].hist(df_privileged['creditworthiness_score'].dropna(), bins=30, color='skyblue', edgecolor='black')
axes[0].axvline(10, color='blue', linestyle='--', label='Threshold = 10')
axes[0].set_title("Privileged Group (Age ≤ Median)")
axes[0].set_xlabel("Creditworthiness Score")
axes[0].set_ylabel("Applicants")
axes[0].legend()
axes[0].grid(True)

axes[1].hist(df_unprivileged['creditworthiness_score'].dropna(), bins=30, color='orange', edgecolor='black')
axes[1].axvline(11, color='red', linestyle='--', label='Threshold = 11')
axes[1].set_title("Unprivileged Group (Age > Median)")
axes[1].set_xlabel("Creditworthiness Score")
axes[1].legend()
axes[1].grid(True)

plt.suptitle("Creditworthiness Score Distribution by Age Group", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()