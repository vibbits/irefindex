#
# irefaccess.tf - creates VM for accessing the cloud managed postgresql server
#
# This part needs to be run as service account "gce-robot@irefindex.iam.gserviceaccount.com"
#

resource "google_compute_disk" "access-boot" {
  name  = "access-boot"
  image = "debian-cloud/debian-11" # standard postgresql 13
}

resource "google_compute_instance" "access-vm" {
  name                      = local.access-vm
  machine_type              = "e2-standard-2"
  allow_stopping_for_update = true

  metadata = {
    "enable-oslogin" = "TRUE"
  }

  network_interface {
    network = "default"
    access_config {
      # auto ip address
    }
  }

  boot_disk {
    auto_delete = true
    source      = google_compute_disk.access-boot.self_link
  }
  # attached_disk {
  #   source      = google_compute_disk.dataext.self_link
  #   device_name = "dataext"
  # }
}

output "access-vm-external-ip" {
  value = google_compute_instance.access-vm.network_interface[0].access_config[0].nat_ip
}
