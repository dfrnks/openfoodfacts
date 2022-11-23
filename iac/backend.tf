terraform {
  backend "gcs" {
    bucket  = "openfoodfacts-datasets"
    prefix  = "terraform/state"
  }
}