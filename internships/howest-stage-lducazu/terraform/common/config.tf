locals {
  # directories
  basedir    = "/stuff/luc/BIT11-stage/howest-stage-repo"
  secretsdir = "${local.basedir}/secrets"

  # project specific
  project = "irefindex"
  region  = "us-central1"
  zone    = "us-central1-c"

  # VM specific
  build-vm  = "irefbuild"
  access-vm = "irefaccess"

  external_users = [
    "user:alexander.botzki@vib.be",
    "user:paco.hulpiau@howest.be",
  ]
}
