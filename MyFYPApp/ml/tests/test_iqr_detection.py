import pandas as pd

from MyFYPApp.ml.preprocessing.outlier_detection import (
    calculate_iqr_bounds,
    detect_iqr_outliers_with_bounds
)


def main():

    year = 2025

    print("\n========== IQR DETECTION TEST ==========")

    # Step 1: Calculate yearly IQR bounds
    bounds = calculate_iqr_bounds(year)

    # Step 2: Create sample records
    sample_data = pd.DataFrame({

        "item_code": [
            93,
            93,
            93,
            95,
            95
        ],

        "average_price": [
            16.00,
            1600.00,
            5.00,
            10.00,
            1030.00
        ]

    })

    print("\nSample Data:")
    print(sample_data)

    # Step 3: Detect outliers using yearly bounds
    result = detect_iqr_outliers_with_bounds(
        sample_data,
        bounds
    )

    # Step 4: Display results
    print("\n========== TEST RESULTS ==========")

    print(result.to_string(index=False))

    # Step 5: Verify expected results
    expected_high = (
        result["IsIQRHighOutlier"].tolist()
        == [False, True, False, False, True]
    )

    if expected_high:
        print("\nSUCCESS: High outlier detection is correct!")
    else:
        print("\nFAILED: High outlier detection is incorrect!")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()