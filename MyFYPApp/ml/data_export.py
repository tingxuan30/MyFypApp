
import os
import pyarrow as pa
import pyarrow.parquet as pq


class ChunkExporter:

    def __init__(self, output_folder, year):

        self.output_folder = output_folder
        self.year = year

        os.makedirs(output_folder, exist_ok=True)

        # Final output paths
        self.clean_path = os.path.join(
            output_folder,
            f"vegetable_cleaned_{year}.parquet"
        )

        self.anomaly_path = os.path.join(
            output_folder,
            f"vegetable_anomalies_{year}.csv"
        )

        self.full_path = os.path.join(
            output_folder,
            f"vegetable_full_report_{year}.parquet"
        )

        # Temporary output paths
        self.clean_temp = self.clean_path + ".tmp"
        self.anomaly_temp = self.anomaly_path + ".tmp"
        self.full_temp = self.full_path + ".tmp"

        # Remove leftover temporary files
        for path in [
            self.clean_temp,
            self.anomaly_temp,
            self.full_temp
        ]:
            if os.path.exists(path):
                os.remove(path)

        self.clean_writer = None
        self.full_writer = None

        self.first_anomaly_chunk = True
        self.closed = False

    def write_parquet(self, df, path, writer_name):

        if df.empty:
            return

        table = pa.Table.from_pandas(
            df,
            preserve_index=False
        )

        if writer_name == "clean":
            writer = self.clean_writer
        else:
            writer = self.full_writer

        if writer is None:

            writer = pq.ParquetWriter(
                path,
                table.schema,
                compression="snappy"
            )

            if writer_name == "clean":
                self.clean_writer = writer
            else:
                self.full_writer = writer

        writer.write_table(table)

    def write_chunk(
        self,
        clean_df,
        anomaly_df,
        full_df
    ):

        if self.closed:
            raise RuntimeError("Exporter is already closed.")

        # 1. Export clean dataset
        self.write_parquet(
            clean_df,
            self.clean_temp,
            "clean"
        )

        # 2. Export anomaly dataset
        if not anomaly_df.empty:

            anomaly_df.to_csv(
                self.anomaly_temp,
                mode="w" if self.first_anomaly_chunk else "a",
                header=self.first_anomaly_chunk,
                index=False
            )

            self.first_anomaly_chunk = False

        elif self.first_anomaly_chunk:

            # Create CSV with column headers
            anomaly_df.to_csv(
                self.anomaly_temp,
                index=False
            )

            self.first_anomaly_chunk = False

        # 3. Export full report
        self.write_parquet(
            full_df,
            self.full_temp,
            "full"
        )

    def _close_writers(self):

        if self.clean_writer is not None:
            self.clean_writer.close()
            self.clean_writer = None

        if self.full_writer is not None:
            self.full_writer.close()
            self.full_writer = None

    def abort(self):

        if self.closed:
            return

        print("\n========== EXPORT ABORTED ==========")

        try:
            self._close_writers()
        finally:
            for path in [
                self.clean_temp,
                self.anomaly_temp,
                self.full_temp
            ]:
                if os.path.exists(path):
                    os.remove(path)

            self.closed = True

        print("Temporary files removed.")
        print("Previous successful output files preserved.")

    def close(self):

        if self.closed:
            return

        try:

            # Close all Parquet writers
            self._close_writers()

            # Check whether all three temporary files exist
            required_files = [
                self.clean_temp,
                self.anomaly_temp,
                self.full_temp
            ]

            missing_files = [
                path for path in required_files
                if not os.path.exists(path)
            ]

            if missing_files:
                raise RuntimeError(
                    "Export incomplete. Missing temporary files: "
                    + ", ".join(missing_files)
                )

            # Validate Parquet files
            clean_rows = pq.ParquetFile(
                self.clean_temp
            ).metadata.num_rows

            full_rows = pq.ParquetFile(
                self.full_temp
            ).metadata.num_rows

            if clean_rows <= 0 or full_rows <= 0:
                raise RuntimeError(
                    "Exported Parquet files contain no records."
                )

            # Replace final files only after successful export
            os.replace(
                self.clean_temp,
                self.clean_path
            )

            os.replace(
                self.anomaly_temp,
                self.anomaly_path
            )

            os.replace(
                self.full_temp,
                self.full_path
            )

            self.closed = True

            print("\n========== EXPORT COMMITTED ==========")
            print(f"Clean records: {clean_rows:,}")
            print(f"Full report records: {full_rows:,}")
            print(f"Clean dataset: {self.clean_path}")
            print(f"Anomaly dataset: {self.anomaly_path}")
            print(f"Full report: {self.full_path}")

        except Exception:
            self.abort()
            raise
