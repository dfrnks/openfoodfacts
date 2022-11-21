import os
import re
import json
import zlib
import logging
import requests

from io import BytesIO
from datetime import datetime
from collections import OrderedDict

FIELD_MATCHER = re.compile(r'(^[^a-zA-Z])|(\W)')

BUCKET_NAME = os.getenv("BUCKET_NAME", "openfoodfacts-datasets")
FILE_DOWNLOAD = os.getenv("FILE_DOWNLOAD", "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz")

logging.basicConfig(level=logging.WARNING)


def iter_lines(r, chunk_size):
    pending = None

    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

    for chunk in r.iter_content(chunk_size=chunk_size):
        chunk = decompressor.decompress(BytesIO(chunk).read())
        if pending is not None:
            chunk = pending + chunk

        lines = chunk.splitlines()

        if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
            pending = lines.pop()
        else:
            pending = None

        yield from lines

    if pending is not None:
        yield pending


def normalize_dict(json_dict):
    normalized_dict = OrderedDict()
    for key, value in json_dict.items():
        key = FIELD_MATCHER.sub('_', key)
        if isinstance(value, dict):
            value = normalize_dict(value)
        normalized_dict[key] = value
    return normalized_dict


def main():
    with requests.get(FILE_DOWNLOAD, stream=True) as r:
        r.raise_for_status()

        # storage_client = storage.Client()
        # bucket = storage_client.bucket(BUCKET_NAME)
        # filename = FILE_DOWNLOAD.split("/")[-1].split(".")
        #
        # filename = filename[0] + '.' + filename[1]

        # with bucket.blob(filename).open("wb") as f:
        c = 0
        with open("openfoodfacts_10000.jsonl", "wb") as f:
            for chunk in iter_lines(r, chunk_size=8192):
                c = c + 1
                logging.debug(f"Chunk size: {len(chunk)} - {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")

                # write = json.dumps(normalize_dict(json.loads(chunk.decode('utf-8')))) + '\n'
                write = chunk.decode('utf-8') + '\n'

                f.write(write.encode())

                if c > 10000:
                    break

#
# def main():
#     with requests.get(FILE_DOWNLOAD, stream=True) as r:
#         r.raise_for_status()
#
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(BUCKET_NAME)
#         filename = FILE_DOWNLOAD.split("/")[-1].split(".")
#
#         filename = filename[0] + '.' + filename[1]
#
#         with bucket.blob(filename).open("wb") as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)
#                 # f.write(gzip.decompress(chunk))


if __name__ == "__main__":
    main()
