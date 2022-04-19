#%%
import csv
import logging
import urllib
import gzip
import urllib.request
from typing import Any, Dict, List
import boto3
from botocore.exceptions import ClientError
import sys
import threading
from boto3.s3.transfer import TransferConfig

import requests
import ssl
from dotenv import load_dotenv
import os


# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Use Boto 3 managed file transfers to manage multipart uploads to and downloads
from an Amazon S3 bucket.

When the file to transfer is larger than the specified threshold, the transfer
manager automatically uses multipart uploads or downloads. This demonstration
shows how to use several of the available transfer manager settings and reports
thread usage and time to transfer.
"""


class TransferCallback:
    """
    Handle callbacks from the transfer manager.

    The transfer manager periodically calls the __call__ method throughout
    the upload and download process so that it can take action, such as
    displaying progress to the user and collecting data about the transfer.
    """

    def __init__(self, target_size):
        self._target_size = target_size
        self._total_transferred = 0
        self._lock = threading.Lock()
        self.thread_info = {}

    def __call__(self, bytes_transferred):
        """
        The callback method that is called by the transfer manager.

        Display progress during file transfer and collect per-thread transfer
        data. This method can be called by multiple threads, so shared instance
        data is protected by a thread lock.
        """
        thread = threading.current_thread()
        with self._lock:
            self._total_transferred += bytes_transferred
            if thread.ident not in self.thread_info.keys():
                self.thread_info[thread.ident] = bytes_transferred
            else:
                self.thread_info[thread.ident] += bytes_transferred

            target = self._target_size * MB
            sys.stdout.write(
                f"\r{self._total_transferred} of {target} transferred "
                f"({(self._total_transferred / target) * 100:.2f}%)."
            )
            sys.stdout.flush()


def upload_with_default_configuration(
    local_file_path, bucket_name, object_key, file_size_mb
):
    """
    Upload a file from a local folder to an Amazon S3 bucket, using the default
    configuration.
    """
    transfer_callback = TransferCallback(file_size_mb)
    s3.Bucket(bucket_name).upload_file(
        local_file_path, object_key, Callback=transfer_callback
    )
    return transfer_callback.thread_info


def get_exchange_data(start: str) -> List[Dict[str, Any]]:
    """gets up to the last 5 days of data from bitcoincharts"""
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
    """gets the entire history of the data"""
    out_file = "checksize.csv"

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
        logging.error(f"There was an error with the download, {e}")


def upload_to_s3(path:str) -> None:
    """uploads the file to S3"""
    # Initialize in:erfaces
    session = boto3.Session(aws_access_key_id=os.getenv('access-key'), aws_secret_access_key=os.getenv("secret-key"))
    s3Resource = session.resource("s3")
    file_name = path
    bucket = "shaz-bucket"
    object = s3Resource.Object(bucket, "test.csv")
    result = object.put(Body=open(file_name, 'rb'))
    res = result.get('ResponseMetadata')

    if res.get('HTTPStatusCode') == 200:
        print('File Uploaded Successfully')
    else:
        print('File Not Uploaded')


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    session = boto3.Session(aws_access_key_id=os.getenv('access-key'), aws_secret_access_key=os.getenv("secret-key"))
    s3Resource = session.client("s3")
    try:
        response = s3Resource.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    load_dotenv()
    # start = 1609459200 # + i * 46800000
    # 5m = every five minutes
    # get_exchange_data(str(start))

    # ssl certificate has expired
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz"
    # download_file(url)
    upload_file("checksize.csv","shaz-bucket")

if __name__ == "__main__":
    main()

# %%
