# Containerized approach

This repository demonstrates the containerization of the vsc Ansible scripts, providing a portable and reproducible environment for executing Ansible playbooks. Containerization offers several advantages, including isolation, scalability, and consistency across different environments.

## Getting started

Build the container (or pull the public one from `<TODO: ask Alexander or James to publish to a repository>`).

```bash
$ # Run this from the root directory of this project.
$ docker build -t irefindex -f oci/Dockerfile .
```

## Customization

To save the output of the data, you can attach a volume and mount them to the expected data location. All locations are the same as how they would be on the VSC instance.

## What ansible files get used?

The ansible files that get used are the ones from the `../vsc/ansible` directory. As these provide a fully functional script for debian based operating systems.

