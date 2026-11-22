
import pandas as pd


# =====================================================
# 1. KNOWN ANOMALIES
# Six investigated suspected 100x price anomalies
# =====================================================

KNOWN_ANOMALIES = [
    {
        "date": "2025-03-02",
        "item_code": 93,
        "premise_code": 2,
        "expected_price": 1600.00
    },
    {
        "date": "2025-11-09",
        "item_code": 1926,
        "premise_code": 3399,
        "expected_price": 1100.00
    },
    {
        "date": "2025-06-14",
        "item_code": 95,
        "premise_code": 17764,
        "expected_price": 1030.00
    },
    {
        "date": "2025-07-02",
        "item_code": 96,
        "premise_code": 15389,
        "expected_price": 699.00
    },
    {
        "date": "2025-02-24",
        "item_code": 1559,
        "premise_code": 2158,
        "expected_price": 598.00
    },
    {
        "date": "2025-02-28",
        "item_code": 1561,
        "premise_code": 2221,
        "expected_price": 450.00
    }
]


# =====================================================
# 2. KNOWN ANOMALY DETECTION
# =====================================================

def detect_known_anomalies(df):

    df["date"] = pd.to_datetime(df["date"])

    df["IsKnownAnomaly"] = False

    conditions = []

    for anomaly in KNOWN_ANOMALIES:

        condition = (
            (df["date"] == pd.Timestamp(anomaly["date"])) &
            (df["item_code"] == anomaly["item_code"]) &
            (df["premise_code"] == anomaly["premise_code"]) &
            (df["average_price"] == anomaly["expected_price"])
        )

        conditions.append(condition)

    if conditions:

        combined_condition = conditions[0]

        for condition in conditions[1:]:
            combined_condition |= condition

        df.loc[combined_condition, "IsKnownAnomaly"] = True

    return df


# =====================================================
# 3. CALCULATE FULL-YEAR IQR BOUNDS
# =====================================================

def calculate_iqr_bounds(year):

    from sqlalchemy import text
    from database import get_engine

    print("\n========== CALCULATING YEARLY IQR BOUNDS ==========")

    engine = get_engine()

    query = text("""
        SELECT
            item_code,
            average_price
        FROM dbo.DailyVegetablePriceByPremise
        WHERE date >= :start_date
          AND date < :end_date
          AND average_price > 0
    """)

    start_date = f"{year}-01-01"
    end_date = f"{year + 1}-01-01"

    try:

        with engine.connect() as connection:

            price_df = pd.read_sql(
                query,
                connection,
                params={
                    "start_date": start_date,
                    "end_date": end_date
                }
            )

        quartiles = (
            price_df.groupby("item_code")["average_price"]
            .quantile([0.25, 0.75])
            .unstack()
        )

        quartiles.columns = ["Q1", "Q3"]

        quartiles["IQR"] = (
            quartiles["Q3"] - quartiles["Q1"]
        )

        quartiles["LowerBound"] = (
            quartiles["Q1"] - 1.5 * quartiles["IQR"]
        )

        quartiles["UpperBound"] = (
            quartiles["Q3"] + 1.5 * quartiles["IQR"]
        )

        print(f"Year: {year}")
        print(f"Vegetable item groups: {len(quartiles)}")

        print("\nIQR Bound Preview:")
        print(quartiles.head(10))

        print("\n========== IQR BOUNDS COMPLETED ==========")

        return quartiles

    finally:
        engine.dispose()

def detect_iqr_outliers_with_bounds(df, bounds):

    print("\n========== IQR OUTLIER DETECTION ==========")

    # Match each record with its item's IQR bounds
    lower_bound = df["item_code"].map(
        bounds["LowerBound"]
    )

    upper_bound = df["item_code"].map(
        bounds["UpperBound"]
    )

    # Detect low and high outliers
    df["IsIQRLowOutlier"] = (
        df["average_price"] < lower_bound
    )

    df["IsIQRHighOutlier"] = (
        df["average_price"] > upper_bound
    )

    low_count = int(df["IsIQRLowOutlier"].sum())
    high_count = int(df["IsIQRHighOutlier"].sum())

    print(f"Low outliers: {low_count:,}")
    print(f"High outliers: {high_count:,}")

    print(
        f"Total IQR outliers: "
        f"{low_count + high_count:,}"
    )

    print("\n========== DETECTION COMPLETED ==========")

    return df

# =====================================================
# 3. IQR OUTLIER DETECTION
# Group by item_code
# =====================================================


def detect_iqr_outliers(df):

    print("\n========== IQR OUTLIER DETECTION ==========")

    # 1. Calculate Q1 and Q3 for each vegetable
    quartiles = (
        df.groupby("item_code")["average_price"]
        .quantile([0.25, 0.75])
        .unstack()
    )

    quartiles.columns = ["Q1", "Q3"]

    # 2. Calculate IQR boundaries
    quartiles["IQR"] = quartiles["Q3"] - quartiles["Q1"]

    quartiles["LowerBound"] = (
        quartiles["Q1"] - 1.5 * quartiles["IQR"]
    )

    quartiles["UpperBound"] = (
        quartiles["Q3"] + 1.5 * quartiles["IQR"]
    )

    # 3. Map boundaries to each record
    lower_bound = df["item_code"].map(
        quartiles["LowerBound"]
    )

    upper_bound = df["item_code"].map(
        quartiles["UpperBound"]
    )

    # 4. Identify low and high outliers
    df["IsIQRLowOutlier"] = (
        df["average_price"] < lower_bound
    )

    df["IsIQRHighOutlier"] = (
        df["average_price"] > upper_bound
    )

    # 5. Display summary
    low_count = int(df["IsIQRLowOutlier"].sum())
    high_count = int(df["IsIQRHighOutlier"].sum())

    print(f"Low outliers: {low_count:,}")
    print(f"High outliers: {high_count:,}")
    print(f"Total IQR outliers: {low_count + high_count:,}")

    print("\n========== DETECTION COMPLETED ==========")

    return df



# =====================================================
# 4. COMBINE OUTLIER DETECTION
# =====================================================

def detect_all_outliers(df):

    print("\n========== OUTLIER DETECTION ==========")

    print("\n1. Detecting known anomalies...")

    df = detect_known_anomalies(df)

    known_count = df["IsKnownAnomaly"].sum()

    print(f"Known anomalies detected: {known_count}")

    print("\n2. Performing IQR detection...")

    df = detect_iqr_outliers(df)

    low_count = df["IsIQRLowOutlier"].sum()

    high_count = df["IsIQRHighOutlier"].sum()

    total_iqr = (
        df["IsIQRLowOutlier"] |
        df["IsIQRHighOutlier"]
    ).sum()

    print(f"Low outliers: {low_count}")

    print(f"High outliers: {high_count}")

    print(f"Total IQR outliers: {total_iqr}")

    print("\n========== DETECTION COMPLETED ==========")

    return df
