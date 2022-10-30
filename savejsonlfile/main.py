import os
import gzip
import logging
import requests
from datetime import datetime
from google.cloud import storage

BUCKET_NAME = os.getenv("BUCKET_NAME", "openfoodfacts-datasets")
FILE_DOWNLOAD = os.getenv("FILE_DOWNLOAD", "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz")
# "https://storage.googleapis.com/openfoodfacts-datasets/tes.txt.gz"


def main():
    with requests.get(FILE_DOWNLOAD, stream=True) as r:
        r.raise_for_status()

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        filename = FILE_DOWNLOAD.split("/")[-1].split(".")
        blob = bucket.blob(filename[0] + '.' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '.' + filename[1] + '.' + filename[2])
        # blob = bucket.blob(filename[0] + '.' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '.' + filename[1])
        with blob.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                logging.info(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
                f.write(chunk)
                # f.write(gzip.decompress(chunk))


if __name__ == "__main__":
    main()
