
from outlier_detection import calculate_iqr_bounds


def main():

    year = 2025

    print("\n========== YEARLY IQR BOUND TEST ==========")

    # Calculate yearly IQR bounds
    bounds = calculate_iqr_bounds(year)

    # Display results
    print("\n========== TEST RESULTS ==========")

    print(f"Year: {year}")
    print(f"Total vegetable groups: {len(bounds)}")

    print("\nFirst 10 vegetable IQR bounds:")
    print(bounds.head(10).to_string())

    # Check required columns
    required_columns = [
        "Q1",
        "Q3",
        "IQR",
        "LowerBound",
        "UpperBound"
    ]

    if all(column in bounds.columns for column in required_columns):
        print("\nSUCCESS: All IQR columns generated!")
    else:
        print("\nFAILED: Missing IQR columns!")

    # Check missing values
    if not bounds[required_columns].isnull().any().any():
        print("SUCCESS: No missing IQR values!")
    else:
        print("WARNING: Some IQR values are missing!")

    # Check calculation logic
    valid_iqr = (
        bounds["IQR"] == bounds["Q3"] - bounds["Q1"]
    ).all()

    if valid_iqr:
        print("SUCCESS: IQR calculation is correct!")
    else:
        print("FAILED: IQR calculation is incorrect!")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
