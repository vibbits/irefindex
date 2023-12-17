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

## Ansible

### Setup

Make sure you have installed ansible on your machine, this machine will act as a human and interact with the infrastructure that has been created by the terraform code. 

The `main1.yml` playbook should be automatically run by terraform. The `main2.yml` and `main3.yml` playbooks should be run manually after the first playbook has finished. And any potential errors have been resolved.

### Using the ansible

Running any of the playbooks can be done by the following command: *(you may have to change some values depending on your `./terraform/irefindex.auto.tfvars` file configuration)*

```bash
ansible-playbook -i '193.190.80.24:50022,' -u 'debian' --private-key=~/.ssh/id_ed25519 ansible/<playbook>.yml
```

### Adding/removing sources from runs

All sources *(and other variables)* are located in the `./ansible/vars/` directory. The `sources.yml` file contains all the sources that will be used. The properties of that source can fully control the whole process of that source from start to finish.

This dynamic aproach also means that adding new sources can simply be done by adding a new line to the `sources.yml` file. And removing a source can be done by removing the line from the `sources.yml` file.

#### Reccomended approach for handing issues that only affect certain sources

If you had issues with a certain source; have resolved the issue, and want to rerun the process for that source. You can simply comment out all other sources by adding a `#` before each source that shouldn't be used.

### Error handling

The playbooks provide a more advantagous way of starting the actions by running this in parralel. To prevent that a error for another resource would kill or corrupt another source its process; errors are collected and shown together when all sources have finished their process.

#### Debugging iRefIndex issues

All jobs are logged to the `/data/irdata18/logs/<datetime>/` directory. The `datetime` for that playbook will be printed in the terminal fail message if any errors occur.

The logging is separated for each process using directories. So if you want to debug the `irdownload` process, you can find the logs in the `/data/irdata18/logs/<datetime>/irdownload/` directory.

There can be up to three different filetypes for each item in the directory. 

- `.out` file contains the stdout of the process
- `.err` file contains the stderr of the process 
- `.msg` file contains any extra messages that have been sent to ansible

This allows quick and easy debugging of any issues that may occur.

### Known issues with sources

#### BAR

This resource can not be downloaded, due to infrastructure issues on their side. The resource is still included in the `./ansible/vars/sources.yml` file but will result in an error.




