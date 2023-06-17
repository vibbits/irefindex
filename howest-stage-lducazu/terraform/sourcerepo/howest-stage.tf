#
# repo.tf - creates a Google Source Repo
#

provider "google" {
  project = local.project
}

resource "google_sourcerepo_repository" "howest-stage" {
  name = "howest-stage"

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_sourcerepo_repository_iam_binding" "viewers" {
  repository = google_sourcerepo_repository.howest-stage.name
  role       = "roles/viewer"
  members    = local.external_users
}

output "repo-url" {
  value = google_sourcerepo_repository.howest-stage.url
}
