
import pandas as pd
from sqlalchemy import text
from preprocessing.database import get_engine

def main():

    engine = get_engine()

    query = text("""
        SELECT TOP (500000)
            date,
            item_code,
            premise_code,
            average_price,
            transaction_count
        FROM dbo.DailyVegetablePriceByPremise
        WHERE date >= '2025-01-01'
          AND date < '2026-01-01'
        ORDER BY date, item_code, premise_code
    """)

    try:
        with engine.connect() as connection:

            chunks = []

            print("\n========== CHUNK LOADING TEST ==========")

            for chunk_number, chunk in enumerate(
                pd.read_sql(
                    query,
                    connection,
                    parse_dates=["date"],
                    chunksize=100000
                ),
                start=1
            ):

                chunks.append(chunk)

                print(
                    f"Chunk {chunk_number}: "
                    f"{len(chunk):,} records | "
                    f"Memory: "
                    f"{chunk.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB"
                )

            df = pd.concat(chunks, ignore_index=True)

        print("\n========== TEST RESULTS ==========")

        print(f"Total records: {len(df):,}")

        total_memory = (
            df.memory_usage(deep=True).sum() / (1024 ** 2)
        )

        print(f"Combined DataFrame memory: {total_memory:.2f} MB")

        print("\nData types:")
        print(df.dtypes)

        print("\nSUCCESS: Chunk loading completed!")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
