# openfoodfacts
This is a project to import Open Food Facts database into BigQuery

## https://googlecloudcheatsheet.withgoogle.com/architecture?link=0b7a78f0-57bb-11ed-be93-67e91afbb90a

# Cloud Run
```shell
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t savejsonlfile .
docker tag savejsonlfile us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/savejsonlfile
docker push us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/savejsonlfile


```

```shell
gcloud beta run jobs create savejsonlfile \
    --project openfoodfacts-datasets \
    --image us-central1-docker.pkg.dev/openfoodfacts-datasets/openfoodfacts-datasets/savejsonlfile:latest \
    --tasks 1 \
    --cpu=2 \
    --memory=8Gi \
    --service-account workflow@openfoodfacts-datasets.iam.gserviceaccount.com \
    --set-env-vars FILE_DOWNLOAD=https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz \
    --set-env-vars BUCKET_NAME=openfoodfacts-datasets \
    --max-retries 1 \
    --region us-central1
    
gcloud beta run jobs execute savejsonlfile --region us-central1
```