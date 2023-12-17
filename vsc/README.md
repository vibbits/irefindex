# IRefIndex VSC

This module contains the changes that were neccecary to run and build the irefindex on the VSC. 

## Terraform

### Setup

Setting up your terraform configuration is pretty straightforward, just copy the `irefindex.auto.tfvars.example` file to `irefindex.auto.tfvars` and edit the parameters to your liking.

You can find additional parameter definitions in the `variables.tf` file.

Also download the `clouds.yaml` file from the VSC platform.

### Using the terraform

To use terraform and create a machine, run `terraform init` and `terraform apply`. If you have skipped the copying of the tfvars terraform will prompt you to fill in the neccecary variables.

If you don't want terraform to let you confirm your configuration, add the `-auto-approve` flag to your `terraform apply` command.

To unprovision the machine run `terraform destroy`. Please do note that this will kill any ongoing progress.

### Known problems
#### Irunpack
##### TAXONOMY
gzip: stdin: invalid compressed data--crc error

gzip: stdin: invalid compressed data--length error
tar: Unexpected EOF in archive
tar: Error is not recoverable: exiting now

#### Irmanifest


