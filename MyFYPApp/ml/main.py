
import os

from data_processing import (
    load_vegetable_data,
    check_data_quality
)

from data_cleaning import clean_vegetable_data


# =====================================================
# 1. CONFIGURATION
# =====================================================

YEAR = 2025

OUTPUT_FOLDER = "cleaned_data"


# =====================================================
# 2. CREATE OUTPUT FOLDER
# =====================================================

def create_output_folder():

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )


# =====================================================
# 3. EXPORT DATASETS
# =====================================================

def export_datasets(clean_df, anomaly_df, full_df, year):

    print("\n========== EXPORTING DATA ==========")

    clean_path = os.path.join(
        OUTPUT_FOLDER,
        f"vegetable_cleaned_{year}.csv"
    )

    anomaly_path = os.path.join(
        OUTPUT_FOLDER,
        f"vegetable_anomalies_{year}.csv"
    )

    full_path = os.path.join(
        OUTPUT_FOLDER,
        f"vegetable_full_report_{year}.csv"
    )

    clean_df.to_csv(
        clean_path,
        index=False
    )

    anomaly_df.to_csv(
        anomaly_path,
        index=False
    )

    full_df.to_csv(
        full_path,
        index=False
    )

    print(f"Clean dataset: {clean_path}")
    print(f"Anomaly dataset: {anomaly_path}")
    print(f"Full dataset: {full_path}")

    print("\nExport completed!")


# =====================================================
# 4. MAIN PIPELINE
# =====================================================

def main():

    print("\n========================================")
    print(" VEGETABLE DATA CLEANING PIPELINE")
    print("========================================")

    year = YEAR

    # Step 1: Load data
    print(f"\nLoading vegetable data for {year}...")

    df = load_vegetable_data(year)

    print(f"Loaded records: {len(df)}")

    # Step 2: Basic data quality check
    check_data_quality(df, year)

    # Step 3: Data cleaning and outlier detection
    clean_df, anomaly_df, full_df = clean_vegetable_data(df)

    # Step 4: Export datasets
    create_output_folder()

    export_datasets(
        clean_df,
        anomaly_df,
        full_df,
        year
    )

    # Step 5: Final summary
    print("\n========================================")
    print(" FINAL PIPELINE SUMMARY")
    print("========================================")

    print(f"Year: {year}")
    print(f"Original records: {len(df)}")
    print(f"Clean records: {len(clean_df)}")
    print(f"Anomaly records: {len(anomaly_df)}")

    print("\nPIPELINE COMPLETED SUCCESSFULLY!")


# =====================================================
# 5. RUN PROGRAM
# =====================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as e:

        print("\nPIPELINE ERROR:")
        print(e)
