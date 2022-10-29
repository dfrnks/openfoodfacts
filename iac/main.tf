terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.41.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "openfoodfacts-datasets"
}

resource "google_project_service" "project" {
    project = "openfoodfacts-datasets"
    service = "workflows.googleapis.com"
}