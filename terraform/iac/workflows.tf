resource "google_project_service" "workflows" {
  service = "workflows.googleapis.com"
}

resource "google_project_service" "cloudscheduler" {
  service = "cloudscheduler.googleapis.com"
}

resource "google_workflows_workflow" "import-openfoodfacts-products-to-bigquery" {
  name            = "import-openfoodfacts-products-to-bigquery"
  region          = "us-central1"
  description     = "ETL To import jsonl to bigquery table"
  service_account = google_service_account.workflow.id
  source_contents = file("${path.module}/../../jobs/import-openfoodfacts-products-to-bigquery/workflow.yml")
}

resource "google_cloud_scheduler_job" "import-openfoodfacts-products-to-bigquery" {
  name             = "import-openfoodfacts-products-to-bigquery"
  description      = "import-openfoodfacts-products-to-bigquery"
  schedule         = "0 4  * * 7"
  time_zone        = "America/Sao_Paulo"
  attempt_deadline = "320s"
  region           = var.location

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/${var.project}/locations/${var.location}/workflows/${google_workflows_workflow.import-openfoodfacts-products-to-bigquery.name}/executions"
    body        = base64encode("{\"argument\":\"{}\",\"callLogLevel\":\"LOG_ALL_CALLS\"}")

    oauth_token {
      service_account_email = google_service_account.workflow.email
    }
  }
}

resource "google_workflows_workflow" "execute-dataform" {
  name            = "execute-dataform"
  region          = "us-central1"
  description     = "ETL To create the trusted layer"
  service_account = google_service_account.workflow.id
  source_contents = file("${path.module}/../../jobs/execute-dataform/workflow.yml")
}

resource "google_cloud_scheduler_job" "execute-dataform" {
  name             = "execute-dataform"
  description      = "execute-dataform"
  schedule         = "0 8  * * 7"
  time_zone        = "America/Sao_Paulo"
  attempt_deadline = "320s"
  region           = var.location

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/${var.project}/locations/${var.location}/workflows/${google_workflows_workflow.execute-dataform.name}/executions"
    body        = base64encode("{\"argument\":\"{}\",\"callLogLevel\":\"LOG_ALL_CALLS\"}")

    oauth_token {
      service_account_email = google_service_account.workflow.email
    }
  }
}