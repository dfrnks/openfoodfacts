provider "google" {
  project = "openfoodfacts-datasets"
}

resource "google_project_service" "workflows" {
  service = "workflows.googleapis.com"
}

resource "google_service_account" "workflow" {
  account_id   = "workflow"
  display_name = "Workflow Service Account"
}

resource "google_storage_bucket" "openfoodfacts-datasets" {
  name          = "openfoodfacts-datasets"
  location      = "US"
  force_destroy = true
}

resource "google_storage_bucket_acl" "image-store-acl" {
  bucket = google_storage_bucket.openfoodfacts-datasets.name

  role_entity = [
    "OWNER:user-${google_service_account.workflow.email}",
  ]
}

resource "google_workflows_workflow" "workflow" {
  name            = "workflow"
  region          = "us-central1"
  description     = "Magic"
  service_account = google_service_account.workflow.id
  source_contents = file("${path.module}/../workflow.yaml")
}
