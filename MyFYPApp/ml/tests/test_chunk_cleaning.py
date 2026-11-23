from preprocessing.data_processing import iter_vegetable_data
from preprocessing.outlier_detection import calculate_iqr_bounds
from preprocessing.data_cleaning import clean_vegetable_chunk


def main():

    year = 2025

    print("\n========== CHUNK CLEANING TEST ==========")

    # Step 1: Calculate yearly IQR bounds
    print("\n1. Calculating yearly IQR bounds...")

    bounds = calculate_iqr_bounds(year)

    # Step 2: Load only the first 10,000 records
    print("\n2. Loading sample data...")

    sample_chunk = next(
        iter_vegetable_data(
            year,
            chunksize=10000
        )
    )

    print(f"Sample records: {len(sample_chunk):,}")

    # Step 3: Clean sample chunk
    print("\n3. Cleaning sample data...")

    clean_df, anomaly_df, full_df = clean_vegetable_chunk(
        sample_chunk,
        bounds
    )

    # Step 4: Verify results
    print("\n========== TEST RESULTS ==========")

    print(f"Original records: {len(sample_chunk):,}")
    print(f"Clean records: {len(clean_df):,}")
    print(f"Anomaly records: {len(anomaly_df):,}")
    print(f"Full report records: {len(full_df):,}")

    print(
        "Known anomalies detected:",
        int(full_df["IsKnownAnomaly"].sum())
    )

    print(
        "IQR low outliers:",
        int(full_df["IsIQRLowOutlier"].sum())
    )

    print(
        "IQR high outliers:",
        int(full_df["IsIQRHighOutlier"].sum())
    )

    # Check record counts
    if len(full_df) == len(clean_df) + int(
        full_df["IsKnownAnomaly"].sum()
    ):
        print("\nSUCCESS: Clean dataset count is correct!")
    else:
        print("\nFAILED: Clean dataset count is incorrect!")

    if len(anomaly_df) == int(full_df["IsAnomaly"].sum()):
        print("SUCCESS: Anomaly dataset count is correct!")
    else:
        print("FAILED: Anomaly dataset count is incorrect!")

    # Check required columns
    required_columns = [
        "OriginalPrice",
        "IsKnownAnomaly",
        "IsIQRLowOutlier",
        "IsIQRHighOutlier",
        "IsAnomaly",
        "AnomalyType",
        "AnomalyReason"
    ]

    if all(column in full_df.columns for column in required_columns):
        print("SUCCESS: All cleaning columns generated!")
    else:
        print("FAILED: Missing cleaning columns!")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()