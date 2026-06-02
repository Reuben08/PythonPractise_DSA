import json
import os
import psycopg2
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split


def create_splits(file_path: str, output_dir: str) -> dict:
    """
    Split processed data into train (70%), val (15%), test (15%).

    Stratified by activity_label so every activity class appears proportionally
    in all three splits — prevents a split from being dominated by one activity.
    """
    df = pd.read_csv(file_path)
    os.makedirs(output_dir, exist_ok=True)

    # First cut: 70% train, 30% temp
    train_df, temp_df = train_test_split(
        df, test_size=0.30, stratify=df["activity_label"], random_state=42
    )
    # Second cut: split the 30% evenly into val and test (15% each)
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, stratify=temp_df["activity_label"], random_state=42
    )

    paths = {
        "train": os.path.join(output_dir, "train.csv"),
        "val":   os.path.join(output_dir, "val.csv"),
        "test":  os.path.join(output_dir, "test.csv"),
    }
    train_df.to_csv(paths["train"], index=False)
    val_df.to_csv(paths["val"],     index=False)
    test_df.to_csv(paths["test"],   index=False)

    for split, path in paths.items():
        print(f"{split}: {len(pd.read_csv(path))} rows → {path}")

    return paths


def generate_dataset_card(split_paths: dict, output_dir: str) -> str:
    """
    Write a JSON summary of the curated dataset.

    Dataset cards are standard practice in ML — they document what the dataset
    contains, how it was split, and the class distribution per split.
    ML researchers use this to understand the data before training.
    """
    card = {
        "created_at": datetime.now().isoformat(),
        "modalities": ["sensor", "image_metadata"],
        "source": "UCI HAR Dataset + synthetic image metadata",
        "splits": {},
    }

    for split_name, path in split_paths.items():
        df = pd.read_csv(path)
        card["splits"][split_name] = {
            "num_records": len(df),
            "num_features": len(df.columns),
            "class_distribution": df["activity_label"].value_counts().to_dict(),
        }

    output_path = os.path.join(output_dir, "dataset_card.json")
    with open(output_path, "w") as f:
        json.dump(card, f, indent=2)

    print(f"Dataset card written → {output_path}")
    return output_path


def log_dataset_stats(conn_params: dict, run_id: str, split_paths: dict) -> None:
    """Write per-split statistics to the dataset_stats table in Postgres."""
    conn = psycopg2.connect(**conn_params)
    try:
        with conn.cursor() as cur:
            for split_name, path in split_paths.items():
                df = pd.read_csv(path)
                class_dist = df["activity_label"].value_counts().to_dict()
                cur.execute(
                    """
                    INSERT INTO dataset_stats
                        (run_id, modality, num_records, num_features, class_distribution, split)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        run_id,
                        "sensor+image",
                        len(df),
                        len(df.columns),
                        json.dumps(class_dist),
                        split_name,
                    )
                )
        conn.commit()
        print(f"Logged dataset stats for {len(split_paths)} splits.")
    finally:
        conn.close()
