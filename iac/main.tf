variable "project" {
  default = "openfoodfacts-datasets"
}

variable "location" {
  default = "us-central1"
}

provider "google" {
  project = var.project
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

resource "google_project_iam_member" "run-developer" {
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.workflow.email}"
  project = var.project
}

resource "google_project_iam_member" "cloudscheduler-serviceAgent" {
  role    = "roles/cloudscheduler.serviceAgent"
  member  = "serviceAccount:${google_service_account.workflow.email}"
  project = var.project
}

resource "google_project_iam_member" "workflows-serviceAgent" {
  role    = "roles/workflows.serviceAgent"
  member  = "serviceAccount:${google_service_account.workflow.email}"
  project = var.project
}
