
## How to upload Dataflow job to GCP

```shell
python jobs/import-openfoodfacts-products-to-bigquery/main.py \
--runner DataflowRunner \
--project openfoodfacts-datasets \
--region us-central1 \
--dataflow_service_options=enable_prime \
--temp_location gs://openfoodfacts-datasets/dataflow/temp \
--staging_location gs://openfoodfacts-datasets/dataflow/staging \
--template_location gs://openfoodfacts-datasets/dataflow/import-openfoodfacts-products-to-bigquery
```

```shell
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/download-openfoodfacts-products-jsonl .
docker push us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/download-openfoodfacts-products-jsonl
```

```shell
gcloud builds submit \
--project openfoodfacts-datasets \
--tag us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/import-openfoodfacts-products-to-bigquery:latest .
```

```shell
gcloud dataflow flex-template build gs://openfoodfacts-datasets/dataflow/import-openfoodfacts-products-to-bigquery.json \
--image "us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/import-openfoodfacts-products-to-bigquery:latest" \
--sdk-language "PYTHON" \
--metadata-file "jobs/import-openfoodfacts-products-to-bigquery/metadata.json"
```

```shell
gcloud dataflow flex-template run "import-openfoodfacts-products-to-bigquery-`date +%Y%m%d-%H%M%S`" \
--template-file-gcs-location "gs://openfoodfacts-datasets/dataflow/import-openfoodfacts-products-to-bigquery.json" \
--parameters input="https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz" \
--parameters project="openfoodfacts-datasets" \
--parameters dataset="raw" \
--parameters table="openfoodfacts_json" \
--project="openfoodfacts-datasets" \
--region "us-west1"
```
