import os
import zlib
import logging
import requests

from io import BytesIO
from datetime import datetime
from google.cloud import storage

BUCKET_NAME = os.getenv("BUCKET_NAME", "openfoodfacts-datasets")
FILE_DOWNLOAD = os.getenv("FILE_DOWNLOAD", "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz")
# "https://storage.googleapis.com/openfoodfacts-datasets/tes.txt.gz"

logging.basicConfig(level=logging.WARNING)


def main():
    with requests.get(FILE_DOWNLOAD, stream=True) as r:
        r.raise_for_status()

        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        filename = FILE_DOWNLOAD.split("/")[-1].split(".")

        filename = filename[0] + '.' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '.' + filename[1]

        with bucket.blob(filename).open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                logging.debug(f"Chunk size: {len(chunk)} - {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")

                f.write(decompressor.decompress(BytesIO(chunk).read()))


if __name__ == "__main__":
    main()
