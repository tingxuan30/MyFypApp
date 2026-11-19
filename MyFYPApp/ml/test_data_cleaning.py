
import pandas as pd
from sqlalchemy import text
from database import get_engine
from data_cleaning import clean_vegetable_data


def load_sample_data():

    engine = get_engine()

    query = text("""
        SELECT TOP 994
            date,
            item_code,
            premise_code,
            average_price,
            transaction_count
        FROM dbo.DailyVegetablePriceByPremise
        WHERE date >= '2025-01-01'
          AND date < '2026-01-01'
          AND average_price > 0
        ORDER BY NEWID()
    """)

    try:
        with engine.connect() as connection:
            sample_df = pd.read_sql(
                query,
                connection,
                parse_dates=["date"]
            )
    finally:
        engine.dispose()

    # Retrieve the six investigated anomalies
    anomaly_query = text("""
        SELECT
            date,
            item_code,
            premise_code,
            average_price,
            transaction_count
        FROM dbo.DailyVegetablePriceByPremise
        WHERE
            (date = '2025-03-02' AND item_code = 93 AND premise_code = 2)
            OR
            (date = '2025-11-09' AND item_code = 1926 AND premise_code = 3399)
            OR
            (date = '2025-06-14' AND item_code = 95 AND premise_code = 17764)
            OR
            (date = '2025-07-02' AND item_code = 96 AND premise_code = 15389)
            OR
            (date = '2025-02-24' AND item_code = 1559 AND premise_code = 2158)
            OR
            (date = '2025-02-28' AND item_code = 1561 AND premise_code = 2221)
    """)

    engine = get_engine()

    try:
        with engine.connect() as connection:
            known_df = pd.read_sql(
                anomaly_query,
                connection,
                parse_dates=["date"]
            )
    finally:
        engine.dispose()

    # Combine sample records and known anomalies
    sample_df = pd.concat(
        [sample_df, known_df],
        ignore_index=True
    )

    # Remove duplicate records
    sample_df = sample_df.drop_duplicates(
        subset=["date", "item_code", "premise_code"]
    ).reset_index(drop=True)

    return sample_df


def main():

    print("\n========== SAMPLE DATA CLEANING TEST ==========")

    # 1. Load sample data
    df = load_sample_data()

    print(f"\nSample records loaded: {len(df)}")

    print(
        "Known anomaly records included:",
        df["item_code"].isin(
            [93, 1926, 95, 96, 1559, 1561]
        ).sum()
    )

    # 2. Run complete cleaning process
    clean_df, anomaly_df, full_df = clean_vegetable_data(df)

    # 3. Check known anomalies
    known_count = int(full_df["IsKnownAnomaly"].sum())

    # 4. Check output
    print("\n========== SAMPLE TEST RESULTS ==========")

    print(f"Original sample records: {len(df)}")
    print(f"Full processed records: {len(full_df)}")
    print(f"Clean dataset records: {len(clean_df)}")
    print(f"Anomaly dataset records: {len(anomaly_df)}")

    print(f"Known anomalies detected: {known_count}")

    # 5. Validate cleaning results
    if known_count == 6:
        print("\nSUCCESS: All six known anomalies detected!")
    else:
        print("\nFAILED: Known anomaly count is incorrect!")

    if not clean_df["IsKnownAnomaly"].any():
        print("SUCCESS: Known anomalies excluded from clean dataset!")
    else:
        print("FAILED: Known anomalies remain in clean dataset!")

    if full_df["IsAnomaly"].sum() == len(anomaly_df):
        print("SUCCESS: Anomaly dataset count is correct!")
    else:
        print("FAILED: Anomaly dataset count is incorrect!")

    if len(full_df) == len(clean_df) + known_count:
        print("SUCCESS: Clean dataset record count is correct!")
    else:
        print("FAILED: Clean dataset record count is incorrect!")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
