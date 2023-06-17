#
# project.tf - creates GCP project 'irefindex'
#
# IMPORTANT: This part needs to be run *first*
#
# Run this part as a _real_ user, with a Google account.
# Generate application default credentials (ADC) using
#   $ gcloud auth application-default login
#
# Create the GCP project using
#   $ terraform init
#   $ terraform apply
#

provider "google" {
  project = local.project
}

# GCP Project

resource "google_project" "irefindex" {
  name            = local.project
  project_id      = local.project
  billing_account = sensitive("***REMOVED***")

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_os_login_ssh_public_key" "lducazu-pubkey" {
  project = local.project
  user    = "lducazu@gmail.com"
  key     = file("~/.ssh/id_rsa.pub")
}

# Project settings related to networking
# https://cloud.google.com/sql/docs/postgres/configure-private-services-access and
# https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/sql_postgres_instance_private_ip/main.tf

resource "google_project_service" "networking" {
  service                    = "servicenetworking.googleapis.com"
  disable_dependent_services = true
}

resource "google_compute_network" "default" {
  # This resource is created automatically -- sync state with
  # $ terraform import google_compute_network.default default
  name                    = "default"
  description             = "Default network for the project"
  auto_create_subnetworks = true
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "google-managed-services-default"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 20
  network       = google_compute_network.default.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.default.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# Project settings related to Google Source Repos

resource "google_project_service" "sourcerepo" {
  service                    = "sourcerepo.googleapis.com"
  disable_dependent_services = true
}

# Project settings related to Google Compute Engine (GCE)

resource "google_project_service" "gce" {
  service                    = "compute.googleapis.com"
  disable_dependent_services = true
}

resource "google_service_account" "gce-robot" {
  account_id   = "gce-robot"
  display_name = "GCE Robot"
}

resource "google_project_iam_member" "gce-binding" {
  project = local.project
  role    = "roles/compute.instanceAdmin"
  member  = "serviceAccount:${google_service_account.gce-robot.email}"
}

resource "google_service_account_key" "gce-robot-key" {
  service_account_id = google_service_account.gce-robot.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "local_file" "gce-robot-key-json" {
  content              = sensitive(base64decode(google_service_account_key.gce-robot-key.private_key))
  filename             = "${local.secretsdir}/gce-robot.json"
  file_permission      = "0400"
  directory_permission = "0700"
}

# Project settings related to Google Cloud Storage (GCS)

resource "google_project_service" "gcs" {
  service                    = "storage.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "gce-json" {
  service                    = "storage-api.googleapis.com"
  disable_dependent_services = true
}

resource "google_service_account" "gcs-robot" {
  account_id   = "gcs-robot"
  display_name = "GCS Robot"
}

resource "google_project_iam_member" "gcs-binding" {
  project = local.project
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.gcs-robot.email}"
}

resource "google_service_account_key" "gcs-robot-key" {
  service_account_id = google_service_account.gcs-robot.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "local_file" "gcs-robot-key-json" {
  content              = sensitive(base64decode(google_service_account_key.gcs-robot-key.private_key))
  filename             = "${local.secretsdir}/gcs-robot.json"
  file_permission      = "0400"
  directory_permission = "0700"
}

# Project settings related to Google Cloud SQL

resource "google_project_service" "cloud-sql" {
  service                    = "sqladmin.googleapis.com"
  disable_dependent_services = true
}

resource "google_service_account" "sql-robot" {
  account_id   = "sql-robot"
  display_name = "SQL Robot"
}

resource "google_project_iam_member" "sql-binding" {
  project = local.project
  role    = "roles/cloudsql.admin"
  member  = "serviceAccount:${google_service_account.sql-robot.email}"
}

resource "google_service_account_key" "sql-robot-key" {
  service_account_id = google_service_account.sql-robot.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "local_file" "sql-robot-key-json" {
  content              = sensitive(base64decode(google_service_account_key.sql-robot-key.private_key))
  filename             = "${local.secretsdir}/sql-robot.json"
  file_permission      = "0400"
  directory_permission = "0700"
}
