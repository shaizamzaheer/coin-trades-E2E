#%%
import csv
import logging
import urllib
import gzip
import urllib.request
from typing import Any, Dict, List
import sys

import requests
import ssl

# headers = {"Authorization": "Bearer 519265c1-c502-4b70-b93f-19549435d26a"}


def get_exchange_data(start: str) -> List[Dict[str, Any]]:
    url = (
        f" http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD&start={start}"
    )

    try:
        r = urllib.request.urlopen(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)

    # return (r.json().get('data', []))

    with open("checksize.txt", "w") as opened_file:
        csvfile = csv.reader(r.read().decode().split("\n"))
        opened_file.write(str(list(csvfile)))


def download_file(url):
    out_file = "checksize"

    # Download archive
    try:
        # Read the file inside the .gz archive located at url
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                file_content = uncompressed.read()

        # write to file in binary mode 'wb'
        with open(out_file, "wb") as f:
            f.write(file_content)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # start = 1609459200 # + i * 46800000
    # 5m = every five minutes
    # get_exchange_data(str(start))

    # ssl certificate has expired
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
    download_file(url)

# %%
