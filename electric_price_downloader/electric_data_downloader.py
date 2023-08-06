# https://github.com/EnergieID/entsoe-py
import connect_to_db
import csv_reader
import send_to_server
from entsoe import EntsoePandasClient
import datetime

import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


def download(start: datetime, end: datetime, country_code: str):

    # api-key from .env file
    key = os.getenv("API_TOKEN")
    # dowload dayahead prices from entsoe
    client = EntsoePandasClient(api_key=key)
    dayAheadPrices = client.query_day_ahead_prices(
        country_code, start=start, end=end)

    dayAheadPrices.to_csv(f'data/{country_code}_DayAheadPrices.csv')


def download_fi_dayahead():
    country_code = 'FI'
    # get today's date and add 1 day to it to get tomorrow's electricity prices
    today = pd.Timestamp.today() + datetime.timedelta(days=1)
    # format date to match entsoe's format
    parsedTodayStart = today.strftime("%Y%m%d0000")
    todayEnd = today + datetime.timedelta(days=2)
    parsedTodayEnd = todayEnd.strftime("%Y%m%d2300")
    start = pd.Timestamp(parsedTodayStart, tz='Europe/Helsinki')
    end = pd.Timestamp(parsedTodayEnd, tz='Europe/Helsinki')
    download(start, end, country_code)


def download_manual(start: str, end: str, country_code: str):

    dateFrom = pd.Timestamp(start, tz='Europe/Helsinki')
    dateTo = pd.Timestamp(end, tz='Europe/Helsinki')
    download(dateFrom, dateTo, country_code)


if __name__ == '__main__':
    download_fi_dayahead()
    csv_reader.create_json()
    # send_to_server.send_to_server()
    connect_to_db.import_data_to_db()
