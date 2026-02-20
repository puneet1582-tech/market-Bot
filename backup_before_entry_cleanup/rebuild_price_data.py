import pandas as pd

INPUT_FILE = "data/nse_price_history_corrupted_backup.csv"
OUTPUT_FILE = "data/nse_price_history_clean.csv"

print("Reading header rows...")

# Read first 2 rows only
header = pd.read_csv(INPUT_FILE, nrows=2, header=None, low_memory=False)

symbol_row = header.iloc[1]

# Build column name mapping
columns = ["date"] + list(symbol_row[1:])

print("Preparing output file...")
with open(OUTPUT_FILE, "w") as f:
    f.write("date,symbol,price\n")

print("Starting optimized chunk processing...")

chunk_iter = pd.read_csv(
    INPUT_FILE,
    skiprows=2,
    header=None,
    chunksize=2000,
    low_memory=False
)

for chunk in chunk_iter:
    chunk.columns = columns[:len(chunk.columns)]

    # Melt wide → long
    melted = chunk.melt(
        id_vars=["date"],
        var_name="symbol",
        value_name="price"
    )

    # Drop NaNs
    melted = melted.dropna(subset=["price"])

    # Append to output
    melted.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=False,
        index=False
    )

print("Rebuild completed successfully.")
