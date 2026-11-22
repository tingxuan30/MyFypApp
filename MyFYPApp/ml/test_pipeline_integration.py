
import os
import shutil
import pandas as pd

from data_processing import iter_vegetable_data
from outlier_detection import calculate_iqr_bounds
from data_cleaning import clean_vegetable_chunk
from data_export import ChunkExporter


def main():

    year = 2025
    test_folder = "test_pipeline_output"

    print("\n========== PIPELINE INTEGRATION TEST ==========")

    # 1. Remove previous test output
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)

    # 2. Calculate yearly IQR bounds
    print("\nSTEP 1: Calculating IQR bounds...")

    bounds = calculate_iqr_bounds(year)

    # 3. Load first 10,000 records
    print("\nSTEP 2: Loading sample data...")

    chunk_iterator = iter_vegetable_data(
        year,
        chunksize=10000
    )

    try:
        sample_chunk = next(chunk_iterator)
    finally:
        chunk_iterator.close()

    print(f"Loaded records: {len(sample_chunk):,}")

    # 4. Clean sample data
    print("\nSTEP 3: Cleaning sample data...")

    clean_df, anomaly_df, full_df = clean_vegetable_chunk(
        sample_chunk,
        bounds
    )

    # 5. Export sample data
    print("\nSTEP 4: Exporting sample data...")

    exporter = ChunkExporter(
        test_folder,
        year
    )

    try:
        exporter.write_chunk(
            clean_df,
            anomaly_df,
            full_df
        )
    finally:
        exporter.close()

    # 6. Verify exported files
    print("\nSTEP 5: Verifying exported files...")

    clean_path = os.path.join(
        test_folder,
        f"vegetable_cleaned_{year}.parquet"
    )

    anomaly_path = os.path.join(
        test_folder,
        f"vegetable_anomalies_{year}.csv"
    )

    full_path = os.path.join(
        test_folder,
        f"vegetable_full_report_{year}.parquet"
    )

    clean_result = pd.read_parquet(clean_path)
    anomaly_result = pd.read_csv(anomaly_path)
    full_result = pd.read_parquet(full_path)

    print(f"Clean records: {len(clean_result):,}")
    print(f"Anomaly records: {len(anomaly_result):,}")
    print(f"Full report records: {len(full_result):,}")

    # 7. Verify record counts
    assert len(full_result) == len(sample_chunk)

    assert len(clean_result) == (
        len(full_result)
        - int(full_result["IsKnownAnomaly"].sum())
    )

    assert len(anomaly_result) == int(
        full_result["IsAnomaly"].sum()
    )

    # 8. Verify required columns
    required_columns = [
        "OriginalPrice",
        "IsKnownAnomaly",
        "IsIQRLowOutlier",
        "IsIQRHighOutlier",
        "IsAnomaly",
        "AnomalyType",
        "AnomalyReason"
    ]

    for column in required_columns:
        assert column in full_result.columns

    print("\nSUCCESS: Record counts are correct!")
    print("SUCCESS: All required columns exist!")
    print("SUCCESS: All three datasets exported!")
    print("\n========== INTEGRATION TEST PASSED ==========")


if __name__ == "__main__":
    main()
