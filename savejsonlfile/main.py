import os
import gzip
import requests
from datetime import datetime
from google.cloud import storage

BUCKET_NAME = os.getenv("BUCKET_NAME", "openfoodfacts-datasets")
FILE_DOWNLOAD = os.getenv("FILE_DOWNLOAD", "https://storage.googleapis.com/openfoodfacts-datasets/tes.txt.gz")
URL1 = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"


def main():
    response = requests.get(FILE_DOWNLOAD)
    result = gzip.decompress(response.content)

    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    filename = FILE_DOWNLOAD.split("/")[-1].split(".")
    blob = bucket.blob(filename[0] + '.' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '.' + filename[1])
    with blob.open("wb") as f:
        f.write(result)


if __name__ == "__main__":
    main()
