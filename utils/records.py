import os
from constants import DATA_DIR

RECORDS_FILE = os.path.join(DATA_DIR, "records.txt")

def read_records() -> list[int]:
    if not os.path.exists(RECORDS_FILE):
        return []
    with open(RECORDS_FILE) as f:
        return sorted([int(line.strip()) for line in f if line.strip()], reverse=True)[:5]

def write_records(records: list[int]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RECORDS_FILE, "w") as f:
        for r in records:
            f.write(f"{r}\n")