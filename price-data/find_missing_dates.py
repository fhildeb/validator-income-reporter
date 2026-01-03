import csv
from datetime import datetime, date, timedelta

CSV_FILENAME = "median_lyx_prices_eur.csv"
START_DATE = date(2023, 6, 6)
END_DATE = date(2025, 12, 31)

# Verify completeness of local list of price meridians
def read_dates_from_csv(path: str) -> set[date]:
    # Reads CSV dates into a set of datetime objects
    dates = set()
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "Date" not in reader.fieldnames:
            raise ValueError(f"CSV must contain a 'Date' column. Found: {reader.fieldnames}")

        for row in reader:
            raw = row.get("Date", "").strip()
            if not raw:
                continue
            try:
                dates.add(datetime.strptime(raw, "%Y-%m-%d").date())
            except ValueError:
                continue

    return dates

def daterange(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def main():
    existing_dates = read_dates_from_csv(CSV_FILENAME)

    missing_dates = [
        d for d in daterange(START_DATE, END_DATE)
        if d not in existing_dates
    ]

    if not missing_dates:
        return

    missing_dates.sort()

    # Print out missing dates
    for d in missing_dates:
        print(f"\"{d.isoformat()}\",")


if __name__ == "__main__":
    main()
