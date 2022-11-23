
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