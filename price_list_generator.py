from utility.api_calls import get_coin_price

import csv
from datetime import date, timedelta

OUTPUT_CSV = "local_price_list.csv"

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

def daterange(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


if __name__ == "__main__":
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Date", "Former LYX Price"])

        for d in daterange(START_DATE, END_DATE):
            price = get_coin_price(d)

            if price is None:
                continue

            writer.writerow([d.isoformat(), f"{price:.10f}"])
            f.flush()  # Save progress to file
