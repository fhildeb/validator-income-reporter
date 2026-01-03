from utility.api_calls import get_coin_price

MISSING_DATES = [
"2024-03-03",
"2024-03-09",
"2024-05-06",
]

# Retrieve daily price medians from manual inputs
if __name__ == "__main__":
    for d in MISSING_DATES:
        price = get_coin_price(d)
        print(f"{d},{price}")