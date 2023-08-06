# Script to populate the database with data from the API

import electric_data_downloader
from datetime import datetime
import csv_reader
import send_to_server
import pandas as pd

start: datetime = datetime(2022, 12, 29)
end: datetime = pd.Timestamp.today()

parsedStart = start.strftime("%Y%m%d0000")
parsedEnd = end.strftime("%Y%m%d2300")

country_code = 'FI'
electric_data_downloader.download_manual(parsedStart, parsedEnd, country_code)
csv_reader.create_json()
send_to_server.send_to_server()
