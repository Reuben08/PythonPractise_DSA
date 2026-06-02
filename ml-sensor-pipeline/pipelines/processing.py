import os
import pandas as pd

# Columns that are metadata — excluded from normalization
METADATA_COLS = {"subject_id", "activity_id", "activity_label", "split"}

# Image columns we pull in during the join
IMAGE_COLS = ["quality_score", "is_blurry", "brightness", "resolution"]


def clean_sensor_data(file_path: str, output_dir: str) -> str:
    """
    Drop rows with nulls in key metadata columns and remove exact duplicate rows.
    Sensor feature nulls would corrupt model training; duplicates would bias it.
    """
    df = pd.read_csv(file_path)
    before = len(df)

    df = df.dropna(subset=list(METADATA_COLS))
    df = df.drop_duplicates()

    print(f"Clean: {before} → {len(df)} rows ({before - len(df)} removed)")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sensor_clean.csv")
    df.to_csv(output_path, index=False)
    return output_path


def normalize_features(file_path: str, output_dir: str) -> str:
    """
    Map sensor features from [-1, 1] to [0, 1] using (x + 1) / 2.

    UCI HAR features are already normalised to [-1, 1] by the dataset authors.
    We shift to [0, 1] — a common requirement for neural network inputs.
    Metadata columns are left untouched.
    """
    df = pd.read_csv(file_path)
    feature_cols = [c for c in df.columns if c not in METADATA_COLS]
    df[feature_cols] = (df[feature_cols] + 1) / 2

    output_path = os.path.join(output_dir, "sensor_normalized.csv")
    df.to_csv(output_path, index=False)
    print(f"Normalized {len(feature_cols)} feature columns → {output_path}")
    return output_path


def join_with_image_metadata(sensor_path: str, image_path: str, output_dir: str) -> str:
    """
    Append image quality columns to each sensor row.

    Both files are row-aligned (generated in ingestion with the same row order),
    so we concat horizontally rather than merge — a merge on subject_id + activity_label
    would produce a cartesian product since both keys repeat across many rows.
    """
    sensor_df = pd.read_csv(sensor_path)
    image_df  = pd.read_csv(image_path, usecols=IMAGE_COLS)

    merged = pd.concat(
        [sensor_df.reset_index(drop=True), image_df.reset_index(drop=True)],
        axis=1
    )

    output_path = os.path.join(output_dir, "processed_data.csv")
    merged.to_csv(output_path, index=False)
    print(f"Joined → {output_path}  shape: {merged.shape}")
    return output_path
