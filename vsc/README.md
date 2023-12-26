# IRefIndex VSC

This module contains information about running and building irefindex on the VSC. More information about running the Ansible playbooks on a Docker instance can be found in `../oci`.

## A step by step usage guide

This guide will walk you through the process of provisioning a machine and creating the next version of irefindex.

If you have already done this once on the host machine, you can skip to step [4](#4-provision-the-machine-using-terraform-irinit-and-irdownload).

### 1. Install Terraform and Ansible

This is the only step that is not accomodated by any image or command; as this will depend on your local machine.

You can find the installation guides here:

- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### 2. Clone this repository and navigate to the Terraform directory

```bash
git clone https://github.com/vibbits/irefindex.git
cd irefindex/vsc/terraform
```

### 3. Download your `clouds.yaml` file from the VSC platform

> If you are already signed in, you can skip to step 4 by clicking [here](https://cloud.vscentrum.be/dashboard/identity/application_credentials).

1. Go to the [VSC cloud platform](https://cloud.vscentrum.be) and sign in if you haven't already.

2. On the dashboard open the `Identity` navigation group.

![Cloud overview](./.assets/cloud-overview.jpg)

3. The group will expand and show you items, of those items click on `Application Credentials`.

![Cloud overview zoom into Application Credentials](./.assets/cloud-overview-zoom-identity.jpg)

4. On the Application Credentials page we will need to create new credentials, click on the `Create Application Credential` button.

![Application Credentials page](./.assets/cloud-credentials.jpg)

5. Fill in the form with your desired configuration, and click on the `Create Application Credential` button.

![Application Credentials form](./.assets/cloud-create-credential.jpg)

6. Your credentials will be shown, do not share these with anyone. Click on the `Download clouds.yaml` button to download your `clouds.yaml` file and place this in the `./terraform/` directory.

![Application credential created](./.assets/cloud-credential-created.jpg)

At this point your file structure should look like this.

```bash
└── vsc
    ├── README.md
    ├── ansible
    │   └── # ... (Ansible files)
    └── terraform
        ├── clouds.yaml # <--- This file should be here
        ├── irefindex.auto.tfvars.example
        ├── main.tf
        └── variables.tf
```

### 4. Provision the machine using Terraform + run irinit and irdownload

> Note: This step will take a while, as it will have to download external resources. During this time your host machine must stay connected to the server.

1. Copy the `irefindex.auto.tfvars.example` file to `irefindex.auto.tfvars`.
    > Note: Additional variables can be found in the `variables.tf` file.
    ```bash
    # pwd: irefindex/vsc/terraform
    cp irefindex.auto.tfvars.example irefindex.auto.tfvars
    ```
2. Edit the `irefindex.auto.tfvars` file to your liking, you can find your available machine flavors in [Launch Instance > Flavor](https://cloud.vscentrum.be/dashboard/project/instances).
3. Download Terraform OpenStack provider plugin.
    ```bash
    # pwd: irefindex/vsc/terraform
    terraform init
    ```
4. Run Terraform to provision the machine (and automatically run the `../ansible/main1.yml` playbook).
    > Note: When asked for confirmation, double check that you want to perform this action and type `yes`.

    > If you want to skip the confirmation step, you can add the `-auto-approve` flag to the command.
    ```bash
    # pwd: irefindex/vsc/terraform
    terraform apply
    ```

### 4.1. (Optional) Resolve issues that arise

At the bottom of the previous command, you can see the resources that did fail during the download phase. Look to the log files to see why the download did fail. Try to rerun it automatically with the `../ansible/after_main1.yml` playbook. If it still doesn't work, try to solve the problem(s) manually, be careful, you need to know technical information for this.

Follow the approach in [Adding/removing sources from runs](#addingremoving-sources-from-runs) to comment out all sources except the one you want to re-run, so the ones that did fail.

Then run this  command to re-run the `irdownload` process for these resources/that resource.

```bash
# pwd: irefindex/vsc
ansible-playbook -i '193.190.80.24,' --ssh-extra-args='-p 50022' -u 'debian' --private-key=~/.ssh/id_ed25519 ../ansible/after_main1.yml
```

### 5. Run irunpack, irmanifest and irparse

```bash
# pwd: irefindex/vsc
ansible-playbook -i '193.190.80.24,' --ssh-extra-args='-p 50022' -u 'debian' --private-key=~/.ssh/id_ed25519 ../ansible/main2.yml
```

### 5.1. (Optional) Resolve issues that arise

Right after ending each phase (respectively irunpack, irmanifest and irparse), you can see the resources that did fail during that phase, so it is needed to scroll up a bit in case of irunpack and irmanifest. Look to the log files to see why the resource did fail. Try to rerun it automatically with the `../ansible/after_main2.yml` playbook. If it still doesn't work, try to solve the problem(s) manually, be careful, you need to know technical information for this.

Follow the approach in [Adding/removing sources from runs](#addingremoving-sources-from-runs) to comment out all sources except the one you want to re-run, so the ones that did fail.

Then run this  command to re-download, re-unpack, re-manifest and re-parse these resources/that resource.

```bash
# pwd: irefindex/vsc
ansible-playbook -i '193.190.80.24,' --ssh-extra-args='-p 50022' -u 'debian' --private-key=~/.ssh/id_ed25519 ../ansible/after_main2.yml
```

### 6. Run irimport and irbuild

```bash
# pwd: irefindex/vsc
ansible-playbook -i '193.190.80.24,' --ssh-extra-args='-p 50022' -u 'debian' --private-key=~/.ssh/id_ed25519 ../ansible/main3.yml
```

### 6.1. (Optional) Resolve issues that arise

Right after ending each phase (respectively irimport and irbuild), you can see the resources that did fail during that phase, so it is needed to scroll up a bit in case of irimport. Look to the log files to see why the resource did fail. Try to solve the problems manually, be careful, you need to know technical information for this.

### 7. Destroy the machine

> IMPORTANT: This will destroy the machine and all data on it. Please make sure you exported the end result before running this.

```bash
# pwd: irefindex/vsc/terraform
terraform destroy
```

## Adding/removing sources from runs

All sources *(and other variables)* are located in the `./ansible/vars/` directory. The `sources.yml` file contains all the sources that will be used. The properties of that source can fully control the whole process of that source from start to finish.

This dynamic aproach also means that adding new sources can simply be done by adding a new line to the `sources.yml` file. And removing a source can be done by removing the line from the `sources.yml` file.

### Recommended approach for handling issues that only affect certain sources

If you had issues with a certain source; have resolved the issue, and want to rerun the process for that source. You can simply comment out all other sources by adding a `#` before each source that shouldn't be used.

## Error handling

The playbooks provide a more advantagous way of starting the actions by running this in parralel. To prevent that a error for another resource would kill or corrupt another source its process; errors are collected and shown together when all sources have finished their process.

## Debugging iRefIndex issues

All jobs are logged to the `/data/irdata18/logs/<datetime>/` directory. The `datetime` for that playbook will be printed in the terminal fail message if any errors occur.

The logging is separated for each process using directories. So if you want to debug the `irdownload` process, you can find the logs in the `/data/irdata18/logs/<datetime>/irdownload/` directory.

There can be up to three different filetypes for each item in the directory.

- `.out` file contains the stdout of the process
- `.err` file contains the stderr of the process
- `.msg` file contains any extra messages that have been sent to Ansible

This allows quick and easy debugging of any issues that may occur.

## Known issues with sources

If a source could be resolved automatically or manually, we will not mention it here. Only the sources for which no solution was found in any way are listed below.

### IRDOWNLOAD

- BAR can not be downloaded, due to infrastructure issues on their side. The resource is still included in the `./ansible/vars/sources.yml` file but will result in an error.
- INNATEDB can not be downloaded, due to infrastructure issues on their side. The resource is still included in the `./ansible/vars/sources.yml` file but will result in an error.
- IPI can not be downloaded, due to infrastructure issues on their side. The resource is still included in the `./ansible/vars/sources.yml` file but will result in an error.
- CORUM can not be downloaded, due to infrastructure issues on their side. The resource is still included in the `./ansible/vars/sources.yml` file but will result in an error.

### IRPARSE

- BIND_TRANSLATION isn't well-formed because of an external problem.
- PDB parsing failed with error -3 while decompressing data.
