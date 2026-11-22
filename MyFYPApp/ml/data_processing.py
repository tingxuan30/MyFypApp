import pandas as pd
from sqlalchemy import text
from database import get_engine



def load_vegetable_data(year, chunksize=200000):

    engine = get_engine()

    query = text("""
        SELECT
            date,
            item_code,
            premise_code,
            average_price,
            transaction_count
        FROM dbo.DailyVegetablePriceByPremise
        WHERE date >= :start_date
          AND date < :end_date
        ORDER BY date, item_code, premise_code
    """)

    start_date = f"{year}-01-01"
    end_date = f"{year + 1}-01-01"

    try:
        with engine.connect() as connection:

            chunks = []

            for chunk in pd.read_sql(
                query,
                connection,
                params={
                    "start_date": start_date,
                    "end_date": end_date
                },
                parse_dates=["date"],
                chunksize=chunksize
            ):

                chunks.append(chunk)

                print(
                    f"Loaded records: "
                    f"{sum(len(c) for c in chunks):,}"
                )

            df = pd.concat(chunks, ignore_index=True)

        return df

    finally:
        engine.dispose()

def iter_vegetable_data(year, chunksize=200000):

    from sqlalchemy import text

    engine = get_engine()

    query = text("""
        SELECT
            date,
            item_code,
            premise_code,
            average_price,
            transaction_count
        FROM dbo.DailyVegetablePriceByPremise
        WHERE date >= :start_date
          AND date < :end_date
        ORDER BY date, item_code, premise_code
    """)

    start_date = f"{year}-01-01"
    end_date = f"{year + 1}-01-01"

    try:

        with engine.connect() as connection:

            for chunk_number, chunk in enumerate(
                pd.read_sql(
                    query,
                    connection,
                    params={
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    parse_dates=["date"],
                    chunksize=chunksize
                ),
                start=1
            ):

                print(
                    f"Loaded Chunk {chunk_number}: "
                    f"{len(chunk):,} records"
                )

                yield chunk

    finally:
        engine.dispose()

def check_data_quality(df, year):

    print("\n========== DATA QUALITY REPORT ==========")

    # 1. Total Records
    print("\n1. Total Records:")
    print(len(df))

    # 2. Missing Values
    print("\n2. Missing Values:")
    print(df.isnull().sum())

    # 3. Duplicate Records
    print("\n3. Duplicate Records:")

    duplicate_count = df.duplicated(
        subset=["date", "item_code", "premise_code"]
    ).sum()

    print(duplicate_count)

    # 4. Invalid Prices
    print("\n4. Invalid Prices:")

    invalid_prices = df[df["average_price"] <= 0]

    print(f"Invalid price records: {len(invalid_prices)}")

    # 5. Invalid Dates
    print("\n5. Invalid Dates:")

    invalid_dates = df[
        df["date"].dt.year != year
    ]

    print(f"Invalid date records: {len(invalid_dates)}")

    # 6. Price Statistics
    print("\n6. Price Statistics:")

    print(df["average_price"].describe())

    print("\n========== CHECK COMPLETED ==========")


def detect_outliers_iqr(df):

    print("\n========== IQR OUTLIER DETECTION ==========")

    # 1. Calculate Q1 and Q3 separately for each vegetable
    quartiles = (
        df.groupby("item_code")["average_price"]
        .quantile([0.25, 0.75])
        .unstack()
    )

    quartiles.columns = ["Q1", "Q3"]

    # 2. Calculate IQR
    quartiles["IQR"] = quartiles["Q3"] - quartiles["Q1"]

    # 3. Calculate lower and upper bounds
    quartiles["LowerBound"] = (
        quartiles["Q1"] - 1.5 * quartiles["IQR"]
    )

    quartiles["UpperBound"] = (
        quartiles["Q3"] + 1.5 * quartiles["IQR"]
    )

    # 4. Match each record with its vegetable's bounds
    lower_bound = df["item_code"].map(
        quartiles["LowerBound"]
    )

    upper_bound = df["item_code"].map(
        quartiles["UpperBound"]
    )

    # 5. Identify potential outliers
    outlier_mask = (
        (df["average_price"] < lower_bound) |
        (df["average_price"] > upper_bound)
    )

    # 6. Count outliers by vegetable
    outlier_summary = (
        df.loc[outlier_mask]
        .groupby("item_code")
        .agg(
            OutlierCount=("average_price", "size"),
            MinimumOutlierPrice=("average_price", "min"),
            MaximumOutlierPrice=("average_price", "max")
        )
        .reset_index()
    )

    # 7. Calculate total records by vegetable
    total_summary = (
        df.groupby("item_code")
        .size()
        .reset_index(name="TotalRecords")
    )

    # 8. Combine summaries
    outlier_summary = total_summary.merge(
        outlier_summary,
        on="item_code",
        how="left"
    )

    outlier_summary["OutlierCount"] = (
        outlier_summary["OutlierCount"]
        .fillna(0)
        .astype("int64")
    )

    outlier_summary["OutlierPercentage"] = (
        outlier_summary["OutlierCount"] /
        outlier_summary["TotalRecords"] * 100
    )

    # 9. Sort by number of outliers
    outlier_summary = outlier_summary.sort_values(
        by="OutlierCount",
        ascending=False
    )

    # 10. Display results
    total_outliers = int(outlier_mask.sum())

    print(f"\nTotal Records: {len(df):,}")
    print(f"Potential Outliers: {total_outliers:,}")

    print(
        f"Outlier Percentage: "
        f"{total_outliers / len(df) * 100:.4f}%"
    )

    print("\nOutlier Summary by Vegetable:")

    print(
        outlier_summary.to_string(index=False)
    )

    print("\n========== DETECTION COMPLETED ==========")

    return outlier_summary


def analyse_outlier_directions(df):

    print("\n========== OUTLIER DIRECTION ANALYSIS ==========")

    # 1. Calculate IQR for each vegetable
    quartiles = (
        df.groupby("item_code")["average_price"]
        .quantile([0.25, 0.75])
        .unstack()
    )

    quartiles.columns = ["Q1", "Q3"]

    quartiles["IQR"] = quartiles["Q3"] - quartiles["Q1"]

    quartiles["LowerBound"] = (
        quartiles["Q1"] - 1.5 * quartiles["IQR"]
    )

    quartiles["UpperBound"] = (
        quartiles["Q3"] + 1.5 * quartiles["IQR"]
    )

    # 2. Match bounds with each record
    lower_bound = df["item_code"].map(
        quartiles["LowerBound"]
    )

    upper_bound = df["item_code"].map(
        quartiles["UpperBound"]
    )

    # 3. Separate low and high outliers
    low_mask = df["average_price"] < lower_bound
    high_mask = df["average_price"] > upper_bound

    # 4. Count low outliers
    low_counts = (
        df.loc[low_mask]
        .groupby("item_code")
        .size()
        .rename("LowOutlierCount")
    )

    # 5. Count high outliers
    high_counts = (
        df.loc[high_mask]
        .groupby("item_code")
        .size()
        .rename("HighOutlierCount")
    )

    # 6. Count total records
    summary = (
        df.groupby("item_code")
        .size()
        .rename("TotalRecords")
        .to_frame()
    )

    # 7. Combine results
    summary = summary.join(low_counts).join(high_counts)

    summary = summary.fillna(0)

    summary["LowOutlierCount"] = (
        summary["LowOutlierCount"].astype("int64")
    )

    summary["HighOutlierCount"] = (
        summary["HighOutlierCount"].astype("int64")
    )

    summary["TotalOutliers"] = (
        summary["LowOutlierCount"] +
        summary["HighOutlierCount"]
    )

    summary["OutlierPercentage"] = (
        summary["TotalOutliers"] /
        summary["TotalRecords"] * 100
    )

    # 8. Load vegetable names from SQL Server
    engine = get_engine()

    try:
        with engine.connect() as connection:

            item_lookup = pd.read_sql(
                text("""
                    SELECT item_code, item
                    FROM dbo.lookup_item
                """),
                connection
            )

    finally:
        engine.dispose()

    # 9. Add vegetable names
    summary = summary.reset_index()

    summary = summary.merge(
        item_lookup,
        on="item_code",
        how="left"
    )

    # 10. Sort by total outlier count
    summary = summary.sort_values(
        by="TotalOutliers",
        ascending=False
    )

    # 11. Display result
    print("\nOutlier Direction Summary:")

    print(
        summary[
            [
                "item_code",
                "item",
                "TotalRecords",
                "LowOutlierCount",
                "HighOutlierCount",
                "TotalOutliers",
                "OutlierPercentage"
            ]
        ].to_string(index=False)
    )

    print("\n========== ANALYSIS COMPLETED ==========")

    return summary


def extract_outlier_samples(df):

    print("\n========== OUTLIER SAMPLE INVESTIGATION ==========")

    selected_items = [
        95, 1926, 96, 1559, 1819,
        1560, 1561, 93, 1396, 1923
    ]

    # 1. Calculate IQR bounds
    quartiles = (
        df.groupby("item_code")["average_price"]
        .quantile([0.25, 0.75])
        .unstack()
    )

    quartiles.columns = ["Q1", "Q3"]

    quartiles["IQR"] = quartiles["Q3"] - quartiles["Q1"]

    quartiles["LowerBound"] = (
        quartiles["Q1"] - 1.5 * quartiles["IQR"]
    )

    quartiles["UpperBound"] = (
        quartiles["Q3"] + 1.5 * quartiles["IQR"]
    )

    # 2. Filter selected vegetables
    sample_df = df[
        df["item_code"].isin(selected_items)
    ].copy()

    sample_df["LowerBound"] = sample_df["item_code"].map(
        quartiles["LowerBound"]
    )

    sample_df["UpperBound"] = sample_df["item_code"].map(
        quartiles["UpperBound"]
    )

    # 3. Identify anomaly direction
    sample_df["AnomalyType"] = "Normal"

    sample_df.loc[
        sample_df["average_price"] < sample_df["LowerBound"],
        "AnomalyType"
    ] = "Low"

    sample_df.loc[
        sample_df["average_price"] > sample_df["UpperBound"],
        "AnomalyType"
    ] = "High"

    # 4. Keep only outliers
    outliers = sample_df[
        sample_df["AnomalyType"] != "Normal"
    ].copy()

    # 5. Extract 10 highest high outliers per vegetable
    high_samples = (
        outliers[outliers["AnomalyType"] == "High"]
        .sort_values("average_price", ascending=False)
        .groupby("item_code")
        .head(10)
    )

    # 6. Extract 10 lowest low outliers per vegetable
    low_samples = (
        outliers[outliers["AnomalyType"] == "Low"]
        .sort_values("average_price", ascending=True)
        .groupby("item_code")
        .head(10)
    )

    # 7. Combine samples
    investigation = pd.concat(
        [high_samples, low_samples]
    )

    # 8. Load lookup information
    engine = get_engine()

    try:
        with engine.connect() as connection:

            item_lookup = pd.read_sql(
                text("""
                    SELECT item_code, item, unit
                    FROM dbo.lookup_item
                """),
                connection
            )

            premise_lookup = pd.read_sql(
                text("""
                    SELECT
                        premise_code,
                        premise,
                        state,
                        district
                    FROM dbo.lookup_premise
                """),
                connection
            )

    finally:
        engine.dispose()

    # 9. Join vegetable and market information
    investigation = investigation.merge(
        item_lookup,
        on="item_code",
        how="left"
    )

    investigation = investigation.merge(
        premise_lookup,
        on="premise_code",
        how="left"
    )

    # 10. Select useful columns
    investigation = investigation[
        [
            "date",
            "item_code",
            "item",
            "premise_code",
            "premise",
            "state",
            "district",
            "average_price",
            "transaction_count",
            "AnomalyType",
            "LowerBound",
            "UpperBound"
        ]
    ]

    investigation = investigation.sort_values(
        ["item_code", "AnomalyType", "average_price"],
        ascending=[True, True, False]
    )

    # 11. Export investigation samples
    investigation.to_csv(
        "outlier_investigation_samples.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nInvestigation samples extracted!")

    print(f"Total sample records: {len(investigation)}")

    print("\nSamples by anomaly type:")

    print(
        investigation["AnomalyType"].value_counts()
    )

    print("\nSamples by vegetable:")

    print(
        investigation.groupby(
            ["item_code", "item", "AnomalyType"]
        ).size()
    )

    print(
        "\nFile saved: outlier_investigation_samples.csv"
    )

    print("\n========== INVESTIGATION COMPLETED ==========")

    return investigation



def test_load_data():

    year = 2025

    print(f"Loading vegetable data for {year}...")

    df = load_vegetable_data(year)

    print("\nData loaded successfully!")
    print(f"Total records: {len(df)}")

    print("\nFirst 5 records:")
    print(df.head())

    print("\nData information:")
    df.info()

    check_data_quality(df)

    outlier_summary = detect_outliers_iqr(df)

    direction_summary = analyse_outlier_directions(df)

    investigation = extract_outlier_samples(df)


if __name__ == "__main__":
    test_load_data()
