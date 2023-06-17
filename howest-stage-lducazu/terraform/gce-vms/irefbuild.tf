#
# irefbuild.tf -- creates VM for running a local postgresql server
#
# This part needs to be run as service account "gce-robot@irefindex.iam.gserviceaccount.com"
#

resource "google_compute_disk" "build-boot" {
  name  = "build-boot"
  image = "debian-cloud/debian-11" # standard postgresql 13
}

resource "google_compute_disk" "pgdbdisk" {
  name = "pgdbdisk"
  type = "pd-balanced"
  size = "2050"

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_compute_instance" "build-vm" {
  name                      = local.build-vm
  machine_type              = "n2-custom-4-22528" # recommendation via GCloud console
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
    auto_delete = false
    source      = google_compute_disk.build-boot.self_link
  }
  attached_disk {
    source      = google_compute_disk.dataext.self_link
    device_name = "dataext"
  }
  attached_disk {
    source      = google_compute_disk.pgdbdisk.self_link
    device_name = "pgdbdisk"
  }
}

output "build-vm-external-ip" {
  value = google_compute_instance.build-vm.network_interface[0].access_config[0].nat_ip
}
