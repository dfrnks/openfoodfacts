resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
}

resource "google_project_iam_member" "secretmanager_secretAccessor" {
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:service-${var.project_number}@gcp-sa-dataform.iam.gserviceaccount.com"
  project = var.project
}

resource "google_secret_manager_secret" "dataform_github_personal_token" {
  depends_on = [google_project_service.secretmanager]

  secret_id = "dataform_github_personal_token"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "github_personal_token" {
  secret = google_secret_manager_secret.dataform_github_personal_token.id

  secret_data = "change_this_on_gcp_console"
}

data "google_secret_manager_secret_version" "github_personal_token" {
  secret = google_secret_manager_secret.dataform_github_personal_token.secret_id
}

resource "google_dataform_repository" "dataform_repository_openfoodfacts" {
  provider = google-beta
  name     = "openfoodfacts"

  git_remote_settings {
    url                                 = "https://github.com/dfrnks/openfoodfacts.git"
    default_branch                      = "main"
    authentication_token_secret_version = data.google_secret_manager_secret_version.github_personal_token.id
  }
}