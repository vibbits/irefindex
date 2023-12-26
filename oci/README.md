# Containerized approach

This repository demonstrates the containerization of this project, providing a portable and reproducible environment for executing Ansible playbooks. Containerization offers several advantages, including isolation, scalability, and consistency across different environments. These containers can be run on CaaS environments. More information about running the Ansible playbooks on the VSC can be found in `../vsc`.

## Getting started

Build the container.

```bash
$ # Run this from the root directory of this project.
$ docker build -t irefindex -f oci/Dockerfile .
```

## Customization

To save the output of the data, you can attach a volume and mount them to the expected data location. All locations are the same as how they would be on the VSC instance (`../vsc`).

## What Ansible files get used?

The Ansible files that get used are the ones from the `../vsc/ansible` directory. As these provide a fully functional script for Debian based operating systems.

