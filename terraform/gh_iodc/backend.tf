terraform {
  backend "gcs" {
    bucket  = "openfoodfacts-datasets"
    prefix  = "terraform/gh_iodc/state"
  }
}
