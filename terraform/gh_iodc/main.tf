provider "google" {
  project = var.project_id
}

resource "google_project_service" "cloudresourcemanager" {
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "iam" {
  service = "iam.googleapis.com"
}

resource "google_project_service" "iamcredentials" {
  service = "iamcredentials.googleapis.com"
}

resource "google_project_service" "sts" {
  service = "sts.googleapis.com"
}

resource "google_service_account" "deploy_service_account" {
  account_id   = "deploy-service-account"
  display_name = "Deploy GH Service Account"
}

resource "google_project_iam_member" "editor" {
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.deploy_service_account.email}"
  project = var.project_id
}

resource "google_project_iam_member" "secretmanager_secret_accessor" {
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.deploy_service_account.email}"
  project = var.project_id
}

resource "google_project_iam_member" "cloudbuild_builds" {
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${google_service_account.deploy_service_account.email}"
  project = var.project_id
}

module "gh_oidc" {
  depends_on = [google_service_account.deploy_service_account]

  source      = "terraform-google-modules/github-actions-runners/google//modules/gh-oidc"
  project_id  = var.project_id
  pool_id     = "openfoodfacts-auth-pool"
  provider_id = "auth-gh-provider"
  sa_mapping  = {
    "deploy-service-account" = {
      sa_name   = "projects/${var.project_id}/serviceAccounts/deploy-service-account@${var.project_id}.iam.gserviceaccount.com"
      attribute = "attribute.repository/${var.gh_user}/${var.gh_repo}"
    }
  }
}

output "workload_identity_provider" {
  value = module.gh_oidc.provider_name
}

output "service_account" {
  value = google_service_account.deploy_service_account.email
}