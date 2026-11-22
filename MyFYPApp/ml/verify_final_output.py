
import os
import pandas as pd
import pyarrow.parquet as pq

folder = "cleaned_data"
year = 2025

clean_path = os.path.join(
    folder, f"vegetable_cleaned_{year}.parquet"
)

anomaly_path = os.path.join(
    folder, f"vegetable_anomalies_{year}.csv"
)

full_path = os.path.join(
    folder, f"vegetable_full_report_{year}.parquet"
)

print("\n========== FINAL OUTPUT VERIFICATION ==========")

# STEP 1: Check file existence
for path in [clean_path, anomaly_path, full_path]:
    assert os.path.exists(path), f"Missing file: {path}"
    print(f"Found: {path}")

# STEP 2: Read Parquet record counts
clean_rows = pq.ParquetFile(clean_path).metadata.num_rows
full_rows = pq.ParquetFile(full_path).metadata.num_rows

# STEP 3: Count CSV records
anomaly_rows = len(pd.read_csv(anomaly_path))

print("\n========== RECORD COUNTS ==========")
print(f"Clean records: {clean_rows:,}")
print(f"Anomaly records: {anomaly_rows:,}")
print(f"Full report records: {full_rows:,}")

# STEP 4: Verify known anomaly flags
full_df = pd.read_parquet(
    full_path,
    columns=["IsKnownAnomaly", "IsAnomaly"]
)

clean_df = pd.read_parquet(
    clean_path,
    columns=["IsKnownAnomaly"]
)

known_in_full = int(full_df["IsKnownAnomaly"].sum())
known_in_clean = int(clean_df["IsKnownAnomaly"].sum())

print("\n========== KNOWN ANOMALY CHECK ==========")
print(f"Known anomalies in full report: {known_in_full}")
print(f"Known anomalies in clean dataset: {known_in_clean}")

# STEP 5: Validate all results
assert clean_rows == 7_745_717, "Clean record count mismatch!"
assert anomaly_rows == 191_948, "Anomaly record count mismatch!"
assert full_rows == 7_745_723, "Full report count mismatch!"

assert known_in_full == 6, "Known anomaly count mismatch!"
assert known_in_clean == 0, "Known anomalies found in clean dataset!"

assert int(full_df["IsAnomaly"].sum()) == anomaly_rows, \
    "IsAnomaly count does not match anomaly CSV!"

print("\nSUCCESS: All record counts are correct!")
print("SUCCESS: All six known anomalies are retained in full report!")
print("SUCCESS: No known anomalies remain in clean dataset!")

print("\n========== FINAL VERIFICATION PASSED ==========")
