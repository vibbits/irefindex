#
# postgres.tf - creates a postgesql instance
#
# This part needs to be run as service account "sql-robot@irefindex.iam.gserviceaccount.com"
#

provider "google" {
  project     = local.project
  region      = local.region
  zone        = local.zone
  credentials = file("${local.secretsdir}/sql-robot.json")
}

# Create database instance

resource "google_sql_database_instance" "pg-irdata19" {
  name             = "pgirdata19"
  region           = "us-central1"
  database_version = "POSTGRES_13"

  # Uncomment the line below if you need to delete the instance
  # deletion_protection = false

  settings {
    tier      = "db-custom-4-26624"
    disk_size = 2000
    ip_configuration {
      ipv4_enabled    = false
      private_network = "projects/irefindex/global/networks/default"
    }
    database_flags {
      name  = "temp_file_limit"
      value = "2147483647"
    }
  }
}

resource "google_sql_user" "lducazu" {
  name     = "lducazu_gmail_com"
  password = sensitive(chomp(file("${local.secretsdir}/pgpasswd")))
  instance = google_sql_database_instance.pg-irdata19.name
}

resource "google_sql_database" "irdata19" {
  name     = "irdata19"
  instance = google_sql_database_instance.pg-irdata19.name
}

output "db-ip" {
  value = google_sql_database_instance.pg-irdata19.first_ip_address
}
