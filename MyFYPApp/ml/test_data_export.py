import os
import shutil
import pandas as pd

from data_export import ChunkExporter


def main():

    test_folder = "test_export"
    year = 2025

    # Remove previous test output
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)

    print("\n========== DATA EXPORT TEST ==========")

    exporter = ChunkExporter(
        test_folder,
        year
    )

    try:

        # Create sample data
        for chunk_number in range(1, 4):

            full_df = pd.DataFrame({

                "date": pd.date_range(
                    start="2025-01-01",
                    periods=3
                ),

                "item_code": [93, 95, 96],

                "average_price": [
                    16.00,
                    10.00,
                    8.00
                ],

                "IsAnomaly": [
                    False,
                    True,
                    False
                ]

            })

            clean_df = full_df.copy()

            anomaly_df = full_df[
                full_df["IsAnomaly"]
            ].copy()

            print(f"\nWriting Chunk {chunk_number}...")

            exporter.write_chunk(
                clean_df,
                anomaly_df,
                full_df
            )

        print("\nAll chunks written successfully!")

    finally:
        exporter.close()

    # Verify exported files
    print("\n========== VERIFYING EXPORTED FILES ==========")

    clean_path = os.path.join(
        test_folder,
        f"vegetable_cleaned_{year}.parquet"
    )

    full_path = os.path.join(
        test_folder,
        f"vegetable_full_report_{year}.parquet"
    )

    anomaly_path = os.path.join(
        test_folder,
        f"vegetable_anomalies_{year}.csv"
    )

    clean_result = pd.read_parquet(clean_path)
    full_result = pd.read_parquet(full_path)
    anomaly_result = pd.read_csv(anomaly_path)

    print(f"Clean records: {len(clean_result)}")
    print(f"Full report records: {len(full_result)}")
    print(f"Anomaly records: {len(anomaly_result)}")

    # Expected results
    if len(clean_result) == 9:
        print("\nSUCCESS: Parquet clean export passed!")
    else:
        print("\nFAILED: Parquet clean export incorrect!")

    if len(full_result) == 9:
        print("SUCCESS: Parquet full report export passed!")
    else:
        print("FAILED: Parquet full report export incorrect!")

    if len(anomaly_result) == 3:
        print("SUCCESS: CSV anomaly export passed!")
    else:
        print("FAILED: CSV anomaly export incorrect!")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()