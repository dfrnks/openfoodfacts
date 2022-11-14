import os
import logging
import requests

from google.cloud import storage

BUCKET_NAME = os.getenv("BUCKET_NAME", "openfoodfacts-datasets")
FILE_DOWNLOAD = os.getenv("FILE_DOWNLOAD", "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz")

logging.basicConfig(level=logging.WARNING)


def main():
    with requests.get(FILE_DOWNLOAD, stream=True) as r:
        r.raise_for_status()

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        filename = FILE_DOWNLOAD.split("/")[-1].split(".")

        filename = filename[0] + '.' + filename[1]

        with bucket.blob(filename).open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


if __name__ == "__main__":
    main()
