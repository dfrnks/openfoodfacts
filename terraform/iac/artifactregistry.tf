resource "google_project_service" "artifactregistry" {
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "cloudbuild" {
  service = "cloudbuild.googleapis.com"
}

resource "google_artifact_registry_repository" "openfoodfacts-datasets" {
  location      = "us-central1"
  repository_id = "openfoodfacts-datasets"
  format        = "DOCKER"
}