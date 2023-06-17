#
# gce.tf - creates data disk, can be attached & mounted on any VM
#
# This part needs to be run as service account "gce-robot@irefindex.iam.gserviceaccount.com"
#

provider "google" {
  project     = local.project
  region      = local.region
  zone        = local.zone
  credentials = file("${local.secretsdir}/gce-robot.json")
}

# VM shared disk

resource "google_compute_disk" "dataext" {
  name = "dataext"
  size = "2050"

  # Restoring a snapshot
  # The GCE robot needs the 'compute.snapshots.useReadonly' permission:
  # $ gcloud compute snapshots add-iam-policy-binding irparse-snapshot \
  #     --member=serviceAccount:gce-robot@irefindex.iam.gserviceaccount.com \
  #     --role=roles/compute.serviceAgent

  # snapshot = "irparse-snapshot"

  lifecycle {
    prevent_destroy = true
  }
}
