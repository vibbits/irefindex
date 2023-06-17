#
# gcs.tf - creates a storage bucket
#
# This part needs to be run as service account "gcs-robot@irefindex.iam.gserviceaccount.com"
#

provider "google" {
  project     = local.project
  region      = local.region
  zone        = local.zone
  credentials = file("${local.secretsdir}/gcs-robot.json")
}

# Create bucket

resource "google_storage_bucket" "irefindex19" {
  name                        = "irefindex19"
  location                    = "US-CENTRAL1"
  uniform_bucket_level_access = true
  force_destroy               = true
}

# External access
resource "google_storage_bucket_iam_binding" "viewers" {
  bucket  = google_storage_bucket.irefindex19.name
  role    = "roles/storage.objectViewer"
  members = local.external_users
}
