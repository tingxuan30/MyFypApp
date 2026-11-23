
import pandas as pd

from MyFYPApp.ml.preprocessing.outlier_detection import detect_all_outliers


# =====================================================
# 1. DATA CLEANING
# =====================================================

def clean_vegetable_data(df):

    print("\n========== DATA CLEANING ==========")

    # Keep original data unchanged
    df = df.copy()

    # Preserve original price
    df["OriginalPrice"] = df["average_price"]

    # Step 1: Basic cleaning
    print("\n1. Checking invalid records...")

    df = df.dropna(
        subset=[
            "date",
            "item_code",
            "premise_code",
            "average_price"
        ]
    )

    df = df[df["average_price"] > 0].copy()

    print(f"Records after basic cleaning: {len(df)}")

    # Step 2: Detect outliers
    print("\n2. Detecting outliers...")

    df = detect_all_outliers(df)

    # Step 3: Create general anomaly flag
    print("\n3. Creating anomaly labels...")

    df["IsAnomaly"] = (
        df["IsKnownAnomaly"] |
        df["IsIQRLowOutlier"] |
        df["IsIQRHighOutlier"]
    )

    # Step 4: Assign anomaly type
    df["AnomalyType"] = "Normal"

    df.loc[
        df["IsIQRLowOutlier"],
        "AnomalyType"
    ] = "Potential Low Price Outlier"

    df.loc[
        df["IsIQRHighOutlier"],
        "AnomalyType"
    ] = "Potential High Price Outlier"

    df.loc[
        df["IsKnownAnomaly"],
        "AnomalyType"
    ] = "Suspected Data Entry Error - 100x"

    # Step 5: Add anomaly reason
    df["AnomalyReason"] = None

    df.loc[
        df["IsIQRLowOutlier"],
        "AnomalyReason"
    ] = "Price below IQR lower bound"

    df.loc[
        df["IsIQRHighOutlier"],
        "AnomalyReason"
    ] = "Price above IQR upper bound"

    df.loc[
        df["IsKnownAnomaly"],
        "AnomalyReason"
    ] = "Investigated isolated price spike, approximately 100x normal price"

    # Step 6: Separate datasets
    print("\n4. Separating normal and anomaly records...")

    anomaly_df = df[df["IsAnomaly"]].copy()

    # Exclude only the six investigated suspected errors
    clean_df = df[~df["IsKnownAnomaly"]].copy()

    print(f"Total records: {len(df)}")
    print(f"Normal / retained records: {len(clean_df)}")
    print(f"All flagged anomaly records: {len(anomaly_df)}")
    print(
        "Known suspected errors excluded: "
        f"{df['IsKnownAnomaly'].sum()}"
    )

    print("\n========== CLEANING COMPLETED ==========")

    return clean_df, anomaly_df, df

def clean_vegetable_chunk(df, bounds):

    print("\n========== CHUNK DATA CLEANING ==========")

    df = df.copy()

    # 1. Preserve original price
    df["OriginalPrice"] = df["average_price"]

    # 2. Basic data cleaning
    df = df.dropna(
        subset=[
            "date",
            "item_code",
            "premise_code",
            "average_price"
        ]
    )

    df = df[df["average_price"] > 0].copy()

    # 3. Detect known anomalies
    from MyFYPApp.ml.preprocessing.outlier_detection import (
        detect_known_anomalies,
        detect_iqr_outliers_with_bounds
    )

    df = detect_known_anomalies(df)

    # 4. Detect IQR outliers using yearly bounds
    df = detect_iqr_outliers_with_bounds(
        df,
        bounds
    )

    # 5. Create anomaly labels
    df["IsAnomaly"] = (
        df["IsKnownAnomaly"] |
        df["IsIQRLowOutlier"] |
        df["IsIQRHighOutlier"]
    )

    df["AnomalyType"] = "Normal"

    df.loc[
        df["IsIQRLowOutlier"],
        "AnomalyType"
    ] = "Potential Low Price Outlier"

    df.loc[
        df["IsIQRHighOutlier"],
        "AnomalyType"
    ] = "Potential High Price Outlier"

    df.loc[
        df["IsKnownAnomaly"],
        "AnomalyType"
    ] = "Suspected Data Entry Error - 100x"

    # 6. Create anomaly reasons
    df["AnomalyReason"] = None

    df.loc[
        df["IsIQRLowOutlier"],
        "AnomalyReason"
    ] = "Price below IQR lower bound"

    df.loc[
        df["IsIQRHighOutlier"],
        "AnomalyReason"
    ] = "Price above IQR upper bound"

    df.loc[
        df["IsKnownAnomaly"],
        "AnomalyReason"
    ] = (
        "Investigated isolated price spike, "
        "approximately 100x normal price"
    )

    # 7. Separate datasets
    anomaly_df = df[df["IsAnomaly"]].copy()

    # Exclude only known suspected errors
    clean_df = df[~df["IsKnownAnomaly"]].copy()

    print("\n========== CHUNK CLEANING SUMMARY ==========")

    print(f"Clean records: {len(clean_df):,}")
    print(f"Anomaly records: {len(anomaly_df):,}")
    print(
        f"Known anomalies: "
        f"{int(df['IsKnownAnomaly'].sum()):,}"
    )

    return clean_df, anomaly_df, df