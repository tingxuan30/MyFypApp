
import pandas as pd
from MyFYPApp.ml.preprocessing.outlier_detection import detect_known_anomalies

# Create test records using the six investigated anomalies
test_data = [
    {
        "date": "2025-03-02",
        "item_code": 93,
        "premise_code": 2,
        "average_price": 1600.00
    },
    {
        "date": "2025-11-09",
        "item_code": 1926,
        "premise_code": 3399,
        "average_price": 1100.00
    },
    {
        "date": "2025-06-14",
        "item_code": 95,
        "premise_code": 17764,
        "average_price": 1030.00
    },
    {
        "date": "2025-07-02",
        "item_code": 96,
        "premise_code": 15389,
        "average_price": 699.00
    },
    {
        "date": "2025-02-24",
        "item_code": 1559,
        "premise_code": 2158,
        "average_price": 598.00
    },
    {
        "date": "2025-02-28",
        "item_code": 1561,
        "premise_code": 2221,
        "average_price": 450.00
    },
    # Normal record: should NOT be identified as known anomaly
    {
        "date": "2025-03-02",
        "item_code": 93,
        "premise_code": 2,
        "average_price": 16.00
    }
]

df = pd.DataFrame(test_data)

# Run known anomaly detection
result = detect_known_anomalies(df)

print("\n========== TEST RESULT ==========")
print(result[
    ["date", "item_code", "premise_code",
     "average_price", "IsKnownAnomaly"]
].to_string(index=False))

# Count detected anomalies
detected_count = int(result["IsKnownAnomaly"].sum())

print(f"\nExpected anomalies: 6")
print(f"Detected anomalies: {detected_count}")

# Validate result
if detected_count == 6:
    print("\nSUCCESS: All six known anomalies detected!")
else:
    print("\nFAILED: Detection count does not match!")

# Check normal record
normal_record = result[
    result["average_price"] == 16.00
]

if not normal_record["IsKnownAnomaly"].iloc[0]:
    print("SUCCESS: Normal record was not flagged!")
else:
    print("FAILED: Normal record was incorrectly flagged!")
