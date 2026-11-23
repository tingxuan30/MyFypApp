
import os
import argparse

from MyFYPApp.ml.preprocessing.data_processing import iter_vegetable_data
from MyFYPApp.ml.preprocessing.outlier_detection import calculate_iqr_bounds
from MyFYPApp.ml.preprocessing.data_cleaning import clean_vegetable_chunk
from MyFYPApp.ml.preprocessing.data_export import ChunkExporter


OUTPUT_FOLDER = "cleaned_data"
CHUNK_SIZE = 200000


def main():

    # 1. Get year from command line
    parser = argparse.ArgumentParser(
        description="Vegetable Data Preprocessing Pipeline"
    )

    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Year to process, e.g. 2025"
    )

    args = parser.parse_args()
    year = args.year

    print("\n========== VEGETABLE DATA PREPROCESSING ==========")
    print(f"Processing Year: {year}")
    print(f"Chunk Size: {CHUNK_SIZE:,}")

    # 2. Calculate yearly IQR bounds
    print("\n========== STEP 1: IQR BOUNDS ==========")

    bounds = calculate_iqr_bounds(year)

    # 3. Initialize exporter
    print("\n========== STEP 2: INITIALIZE EXPORTER ==========")

    exporter = ChunkExporter(
        OUTPUT_FOLDER,
        year
    )

    # 4. Initialize counters
    total_records = 0
    total_clean = 0
    total_anomalies = 0
    total_known = 0
    total_low = 0
    total_high = 0
    total_chunks = 0
    total_invalid = 0

    try:

        # 5. Process data chunk by chunk
        print("\n========== STEP 3: CHUNK PROCESSING ==========")

        for chunk in iter_vegetable_data(
            year,
            chunksize=CHUNK_SIZE
        ):

            total_chunks += 1

            original_count = len(chunk)
            total_records += original_count

            # Count invalid records before cleaning
            valid_mask = (
                chunk[
                    [
                        "date",
                        "item_code",
                        "premise_code",
                        "average_price"
                    ]
                ].notna().all(axis=1)
                & (chunk["average_price"] > 0)
            )

            total_invalid += int((~valid_mask).sum())

            # Clean current chunk
            clean_df, anomaly_df, full_df = clean_vegetable_chunk(
                chunk,
                bounds
            )

            # Update counters
            total_clean += len(clean_df)
            total_anomalies += len(anomaly_df)

            total_known += int(
                full_df["IsKnownAnomaly"].sum()
            )

            total_low += int(
                full_df["IsIQRLowOutlier"].sum()
            )

            total_high += int(
                full_df["IsIQRHighOutlier"].sum()
            )

            # Export current chunk
            exporter.write_chunk(
                clean_df,
                anomaly_df,
                full_df
            )

            print(
                f"\nChunk {total_chunks} completed"
            )

            print(f"Original: {original_count:,}")
            print(f"Clean: {len(clean_df):,}")
            print(f"Anomalies: {len(anomaly_df):,}")

            # Release references to current chunk
            del chunk
            del clean_df
            del anomaly_df
            del full_df

    except Exception:

        print("\n========== PIPELINE FAILED ==========")

        exporter.abort()

        raise

    else:

        if total_chunks == 0:
            exporter.abort()
            raise RuntimeError(
                f"No vegetable records found for year {year}."
            )

        exporter.close()

    # 6. Final summary
    print("\n========== FINAL SUMMARY ==========")

    print(f"Year: {year}")
    print(f"Total chunks: {total_chunks:,}")
    print(f"Original records: {total_records:,}")
    print(f"Invalid records removed: {total_invalid:,}")
    print(f"Clean records: {total_clean:,}")
    print(f"Anomaly records: {total_anomalies:,}")
    print(f"Known anomalies: {total_known:,}")
    print(f"IQR low outliers: {total_low:,}")
    print(f"IQR high outliers: {total_high:,}")

    print("\n========== PREPROCESSING COMPLETED ==========")


if __name__ == "__main__":

    try:
        main()

    except Exception as e:

        print("\nERROR OCCURRED:")
        print(e)
        raise
