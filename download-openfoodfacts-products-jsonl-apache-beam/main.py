import re
import json
import zlib
import argparse
import requests
import apache_beam as beam

from io import BytesIO
from datetime import datetime
from collections import OrderedDict

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class downloadFile(beam.DoFn):
    def iter_lines(self, r, chunk_size):
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

    def process(self, element, *args, **kwargs):
        with requests.get(element, stream=True) as f:
            f.raise_for_status()

            for chunk in self.iter_lines(f, chunk_size=8192):
                yield json.loads(chunk.decode('utf-8'))


class normalizeJson(beam.DoFn):
    def normalize_dict(self, json_dict):
        FIELD_MATCHER = re.compile(r'(^[^a-zA-Z])|(\W)')

        normalized_dict = OrderedDict()
        for key, value in json_dict.items():
            key = FIELD_MATCHER.sub('_', key).lower()
            if re.match(r'(?=ingredients_text_)(.*)(?=_ocr_)(.*)', key):
                result = re.search(r'(?=ingredients_text_)(.*)(?=_ocr_)(.*)', key)
                key = "ingredients_text_ocr_" + result.group(1).split("_")[-1]
            if isinstance(value, dict):
                value = self.normalize_dict(value)
                # value = json.dumps(value)
            elif isinstance(value, list):
                for i, j in enumerate(value):
                    if isinstance(j, dict):
                        value[i] = self.normalize_dict(j)
                        # value[i] = json.dumps(j)
                    elif isinstance(j, list):
                        value[i] = json.dumps(j)
                    elif j is None:
                        value[i] = ""
                    else:
                        value[i] = j

            elif value is None:
                value = ""
            else:
                value = value

            normalized_dict[key] = value
        return normalized_dict

    def process(self, element, *args, **kwargs):
        yield json.dumps(self.normalize_dict(element))


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz'
    )
    parser.add_argument(
        '--output',
        dest='output',
        default='gs://openfoodfacts-datasets/beam/openfoodfacts-products-test2',
        # default='../beam/openfoodfacts-products',
        help='Bucket that the file will be saved'
    )

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Start" >> beam.Create([known_args.input])
            | "Download File" >> beam.ParDo(downloadFile())
            # | 'Normalize' >> beam.ParDo(normalizeJson())
            | 'Create Data Object' >> beam.Map(lambda x: {
                "date": datetime.today().astimezone().isoformat(timespec='minutes'),
                "raw": json.dumps(x)
            })
            # | 'Save Files' >> beam.io.WriteToText(known_args.output, file_name_suffix=".jsonl")
            | 'Save tp BigQuery' >> beam.io.WriteToBigQuery(
                project='openfoodfacts-datasets',
                dataset='test',
                table='import_directly',
                schema='date:TIMESTAMP,raw:STRING',
                # write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        )


if __name__ == "__main__":
    run()
