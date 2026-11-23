
import pandas as pd
from sqlalchemy import text
from preprocessing.database import get_engine
from preprocessing.outlier_detection import detect_known_anomalies

def verify_known_anomalies():

    engine = get_engine()

    query = text("""
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
        ORDER BY date
    """)

    try:
        with engine.connect() as connection:
            df = pd.read_sql(
                query,
                connection,
                parse_dates=["date"]
            )
    finally:
        engine.dispose()

    print("\n========== DATABASE VERIFICATION ==========")

    print(f"Records retrieved: {len(df)}")

    if len(df) == 6:

        result = detect_known_anomalies(df)

        print("\nVerification results:")

        print(
            result[
                [
                    "date",
                    "item_code",
                    "premise_code",
                    "average_price",
                    "IsKnownAnomaly"
                ]
            ].to_string(index=False)
        )

        detected = int(result["IsKnownAnomaly"].sum())

        print(f"\nExpected: 6")
        print(f"Detected: {detected}")

        if detected == 6:
            print("\nSUCCESS: Database verification passed!")
        else:
            print("\nFAILED: Some records were not detected.")

    else:
        print("\nWARNING: Expected 6 records but retrieved", len(df))

if __name__ == "__main__":
    verify_known_anomalies()
