import csv
import json
import numpy as np

# function to convert price to kwH/cent and handle negative and zero values


def calc_price(price: float):
    if price == 0:
        return 0
    elif price < 0:
        print(price)
        minus_price = np.around(price / 10, decimals=3)
        return float(minus_price)
    else:
        plus_price = np.around(price / 10, decimals=3)
        return float(plus_price)

# if price is negative, return the price as it is


def calc_tax(price: float):
    if price == 0:
        return 0
    elif price < 0:
        return price
    else:
        tax = np.around(price * 1.24, decimals=3)
        return float(tax)


def create_json():
    pricesData = []
    try:
        # Open the CSV file using the DictReader
        with open('data/FI_DayAheadPrices.csv', mode="r") as csv_file:

            csv_reader = csv.DictReader(
                csv_file, fieldnames=['datetime', 'price'])
            # skip the first row
            next(csv_reader)
            for row in csv_reader:
                # use calc_price function to convert price to euros and handle negative and zero values
                price = calc_price(float(row['price']))
                priceWithTax = calc_tax(price)

                # Create a dictionary for the row with the modified values
                priceByHourRow = {
                    "datetime": row['datetime'],
                    "pricewithouttax": price,
                    "pricewithtax": priceWithTax,
                }
                pricesData.append(priceByHourRow)
            print(pricesData[0])

    except IOError as e:
        print(f'An error occurred while reading the CSV file: {e}')
        exit(1)

    try:
        with open('data/output_FI_DayAheadPrices.json', 'w') as fp:
            json.dump(pricesData, fp)

    except IOError as e:
        print(f'An error occurred while writing the JSON file: {e}')
        exit(1)
