
https://static.openfoodfacts.org/data/data-fields.txt

# openfoodfacts
This is a project to import Open Food Facts database into BigQuery

## https://googlecloudcheatsheet.withgoogle.com/architecture?link=0b7a78f0-57bb-11ed-be93-67e91afbb90a

# Cloud Run
```shell
cd download-openfoodfacts-products-jsonl
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/download-openfoodfacts-products-jsonl .
docker push us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/download-openfoodfacts-products-jsonl
```

```shell
gcloud beta run jobs create savejsonlfile \
    --project openfoodfacts-datasets \
    --image us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/savejsonlfile:latest \
    --tasks 1 \
    --cpu 2 \
    --memory 8Gi \
    --task-timeout 3600 \
    --service-account workflow@openfoodfacts-datasets.iam.gserviceaccount.com \
    --set-env-vars FILE_DOWNLOAD=https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz \
    --set-env-vars BUCKET_NAME=openfoodfacts-datasets \
    --max-retries 1 \
    --region us-central1
    
gcloud beta run jobs execute savejsonlfile --region us-central1
```











```shell
python main.py \
--runner DataflowRunner \
--project openfoodfacts-datasets \
--region us-central1 \
--dataflow_service_options=enable_prime \
--temp_location gs://openfoodfacts-datasets/dataflow/temp \
--staging_location gs://openfoodfacts-datasets/dataflow/staging \
--template_location gs://openfoodfacts-datasets/dataflow/main
```

```shell
gcloud dataflow jobs run teste \
--project openfoodfacts-datasets \
--region us-central1 \
--gcs-location gs://openfoodfacts-datasets/dataflow/main
```