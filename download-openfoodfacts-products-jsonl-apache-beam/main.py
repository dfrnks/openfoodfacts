import re
import json
import logging
import argparse
import apache_beam as beam

from collections import OrderedDict

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.filesystem import CompressionTypes


logging.basicConfig(level=logging.WARNING)

FIELD_MATCHER = re.compile(r'(^[^a-zA-Z])|(\W)')


def normalize_dict(json_dict):
    normalized_dict = OrderedDict()
    for key, value in json_dict.items():
        key = FIELD_MATCHER.sub('_', key).lower()
        if re.match(r'(?=ingredients_text_)(.*)(?=_ocr_)(.*)', key):
            result = re.search(r'(?=ingredients_text_)(.*)(?=_ocr_)(.*)', key)
            key = "ingredients_text_ocr_" + result.group(1).split("_")[-1]
        if isinstance(value, dict):
            # value = normalize_dict(value)
            value = json.dumps(value)
        elif isinstance(value, list):
            for i, j in enumerate(value):
                if isinstance(j, dict):
                    # value[i] = normalize_dict(j)
                    value[i] = json.dumps(j)
                elif isinstance(j, list):
                    value[i] = json.dumps(j)
                elif j is None:
                    value[i] = ""
                else:
                    value[i] = str(j)

        elif value is None:
            value = ""
        else:
            value = str(value)

        normalized_dict[key] = value
    return normalized_dict


class normalizeJson(beam.DoFn):
    def process(self, element, *args, **kwargs):
        yield json.dumps(normalize_dict(json.loads(element)))


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://openfoodfacts-datasets/openfoodfacts-products.2022-10-30T20:15:11.jsonl.gz',
        # default='gs://openfoodfacts-datasets/openfoodfacts_10000.jsonl.gz',
        # default='../openfoodfacts_10000.jsonl.gz',
        help='Endpoint from OpenFoodFacts Jsonl file'
    )
    parser.add_argument(
        '--output',
        dest='output',
        default='gs://openfoodfacts-datasets/beam/openfoodfacts-products',
        # default='../beam/openfoodfacts-products-10000-2',
        help='Bucket that the file will be saved'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'Read JSON GZ' >> beam.io.ReadFromText(known_args.input, compression_type=CompressionTypes.GZIP)
            | 'normalize' >> beam.ParDo(normalizeJson())
            | 'Save Files' >> beam.io.WriteToText(known_args.output, file_name_suffix=".jsonl")
        )
        p.run()


if __name__ == "__main__":
    run()
