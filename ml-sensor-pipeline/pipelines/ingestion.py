import os
import zipfile
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ── Constants ─────────────────────────────────────────────────────────────────

UCI_HAR_URL = (
    "https://archive.ics.uci.edu/static/public/240"
    "/human+activity+recognition+using+smartphones.zip"
)

# UCI HAR uses integer codes 1-6 for activities. This maps them to readable labels.
ACTIVITY_LABELS = {
    1: "WALKING",
    2: "WALKING_UPSTAIRS",
    3: "WALKING_DOWNSTAIRS",
    4: "SITTING",
    5: "STANDING",
    6: "LAYING",
}


# ── Function 1: Download ──────────────────────────────────────────────────────

def download_uci_har(output_dir: str) -> str:
    """
    Download the UCI HAR zip from the internet and extract it.

    Args:
        output_dir: where to save the zip and extract its contents
                    (maps to data/raw/sensor/ in our project)

    Returns:
        Path to the extracted 'UCI HAR Dataset' folder.
        This return value gets pushed to XCom by the DAG task wrapper
        so the next task knows where to find the raw files.
    """
    os.makedirs(output_dir, exist_ok=True)

    zip_path = os.path.join(output_dir, "uci_har.zip")

    # Skip download if the zip already exists — supports re-runs without re-downloading
    if not os.path.exists(zip_path):
        print(f"Downloading UCI HAR dataset...")
        response = requests.get(UCI_HAR_URL, stream=True, timeout=120)
        response.raise_for_status()  # raises an exception on HTTP errors (4xx, 5xx)

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    else:
        print("Zip already exists, skipping download.")

    # Detect the top-level folder name inside the zip dynamically.
    # The old URL had "UCI HAR Dataset/", the new URL may differ.
    with zipfile.ZipFile(zip_path, "r") as z:
        top_level_dirs = {name.split("/")[0] for name in z.namelist() if "/" in name}
        top_dir = sorted(top_level_dirs)[0]  # take the first (usually only) top-level folder
        extract_path = os.path.join(output_dir, top_dir)

        if not os.path.exists(extract_path):
            print("Extracting zip...")
            z.extractall(output_dir)
            print(f"Extracted to: {extract_path}")
        else:
            print("Already extracted, skipping.")

    return extract_path


# ── Function 2: Parse ─────────────────────────────────────────────────────────

def parse_uci_har(raw_dir: str, output_dir: str) -> str:
    """
    Parse UCI HAR's raw text files into a single structured CSV.

    UCI HAR splits data across many files:
        features.txt         → 561 column names
        train/X_train.txt    → 7,352 rows × 561 sensor feature columns
        train/y_train.txt    → 7,352 activity codes (1-6)
        train/subject_train.txt → 7,352 subject IDs (1-30)
        test/X_test.txt      → 2,947 rows × 561 sensor feature columns
        (same pattern for y_test and subject_test)

    We combine train + test into one CSV with columns:
        subject_id | activity_id | activity_label | split | feature_1 ... feature_561

    Args:
        raw_dir:    path to the extracted 'UCI HAR Dataset' folder
        output_dir: where to write the output CSV

    Returns:
        Path to the output CSV (sensor_data.csv).
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── Step 1: Read feature names ────────────────────────────────────────────
    # features.txt looks like:
    #   1 tBodyAcc-mean()-X
    #   2 tBodyAcc-mean()-Y
    #   ...
    features = pd.read_csv(
        os.path.join(raw_dir, "features.txt"),
        sep=r"\s+",          # whitespace-separated
        header=None,
        names=["idx", "name"]
    )
    feature_names = features["name"].tolist()

    # UCI HAR has duplicate feature names — make them unique by appending a counter
    seen = {}
    unique_names = []
    for name in feature_names:
        if name in seen:
            seen[name] += 1
            unique_names.append(f"{name}_{seen[name]}")
        else:
            seen[name] = 0
            unique_names.append(name)

    # ── Step 2: Load train and test splits ────────────────────────────────────
    dfs = []
    for split in ["train", "test"]:
        split_dir = os.path.join(raw_dir, split)

        # X: 561 sensor features per row
        X = pd.read_csv(
            os.path.join(split_dir, f"X_{split}.txt"),
            sep=r"\s+",
            header=None,
            names=unique_names
        )
        # y: activity code (1-6) per row
        y = pd.read_csv(
            os.path.join(split_dir, f"y_{split}.txt"),
            sep=r"\s+",
            header=None,
            names=["activity_id"]
        )
        # subject: which of the 30 participants produced this row
        subjects = pd.read_csv(
            os.path.join(split_dir, f"subject_{split}.txt"),
            sep=r"\s+",
            header=None,
            names=["subject_id"]
        )

        # Combine side-by-side — all three files have the same number of rows
        df = pd.concat([subjects, y, X], axis=1)
        df["activity_label"] = df["activity_id"].map(ACTIVITY_LABELS)
        df["split"] = split
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)

    output_path = os.path.join(output_dir, "sensor_data.csv")
    full_df.to_csv(output_path, index=False)
    print(f"Parsed {len(full_df):,} records → {output_path}")
    return output_path


# ── Function 3: Generate synthetic image metadata ─────────────────────────────

def generate_image_metadata(sensor_csv_path: str, output_dir: str) -> str:
    """
    Generate synthetic image metadata aligned to the sensor data.

    In a real Apple pipeline, images would be captured alongside sensor readings
    from the same subjects performing the same activities. We simulate this by:
    - Generating one image record per sensor row
    - Using the same subject_id and activity_label as the matching sensor row
    - Randomising realistic image properties (resolution, quality, brightness etc.)

    Args:
        sensor_csv_path: path to sensor_data.csv produced by parse_uci_har
        output_dir:      where to write image_metadata.csv

    Returns:
        Path to image_metadata.csv
    """
    os.makedirs(output_dir, exist_ok=True)

    np.random.seed(42)  # fixed seed so synthetic data is reproducible across runs

    # Only load the columns we need to keep memory usage low
    sensor_df = pd.read_csv(
        sensor_csv_path,
        usecols=["subject_id", "activity_label", "split"]
    )
    n = len(sensor_df)

    base_time = datetime(2023, 1, 1, 8, 0, 0)

    image_metadata = pd.DataFrame({
        "image_id":   [f"IMG_{i:06d}" for i in range(n)],
        "subject_id": sensor_df["subject_id"].values,
        "activity_label": sensor_df["activity_label"].values,
        "split":      sensor_df["split"].values,

        # Realistic resolution distribution: mostly 1080p, some 720p, rare 4K
        "resolution": np.random.choice(
            ["1920x1080", "1280x720", "3840x2160"],
            size=n,
            p=[0.6, 0.3, 0.1]
        ),

        "file_size_kb": np.random.uniform(80, 500, size=n).round(2),

        # Beta distribution skewed toward high quality (most images are good)
        "quality_score": np.random.beta(8, 2, size=n).round(4),

        # 5% of images are blurry — simulates motion blur during activity
        "is_blurry": np.random.choice([True, False], size=n, p=[0.05, 0.95]),

        "brightness": np.random.uniform(40, 220, size=n).round(2),

        # One image captured every 0.5 seconds
        "capture_timestamp": [
            (base_time + timedelta(seconds=i * 0.5)).isoformat()
            for i in range(n)
        ],
    })

    output_path = os.path.join(output_dir, "image_metadata.csv")
    image_metadata.to_csv(output_path, index=False)
    print(f"Generated {n:,} image metadata records → {output_path}")
    return output_path
