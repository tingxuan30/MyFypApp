from preprocessing.data_processing import iter_vegetable_data


def main():

    year = 2025
    total_records = 0
    total_chunks = 0

    print("\n========== CHUNK LOADING TEST ==========")

    for chunk in iter_vegetable_data(
        year,
        chunksize=200000
    ):

        total_chunks += 1
        total_records += len(chunk)

        memory_mb = (
            chunk.memory_usage(deep=True).sum()
            / (1024 ** 2)
        )

        print(
            f"Chunk {total_chunks}: "
            f"{len(chunk):,} records | "
            f"Memory: {memory_mb:.2f} MB"
        )

    print("\n========== TEST RESULTS ==========")

    print(f"Year: {year}")
    print(f"Total chunks: {total_chunks}")
    print(f"Total records: {total_records:,}")

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()