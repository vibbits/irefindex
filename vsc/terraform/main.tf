terraform {
  required_version = ">= 1.6.0"

  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.53.0"
    }
  }
}

provider "openstack" {
  cloud = "openstack"
}


resource "openstack_compute_keypair_v2" "irefindex" {
  name = "${var.base_name}-key"
  public_key = file(var.public_key_path)
}

resource "openstack_networking_port_v2" "irefindex" {
  name           = "${var.base_name}-port"
  network_id     = var.network_id
  admin_state_up = true

  security_group_ids = [
    openstack_compute_secgroup_v2.ssh.id,
  ]
}

resource "openstack_compute_secgroup_v2" "ssh" {
  name        = "${var.base_name}-ssh"
  description = "Allow SSH"

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_instance_v2" "irefindex" {
  name        = var.base_name
  image_name  = var.image_name
  flavor_name = var.flavor_name
  key_pair    = openstack_compute_keypair_v2.irefindex.name

  # Declaring security_groups here does nothing as it gets overwritten by the network.port!
  # To add extra security_groups, use network.port.security_group_ids instead

  network {
    name = var.network_name
    port = openstack_networking_port_v2.irefindex.id
  }
}

resource "openstack_networking_portforwarding_v2" "ssh_pf" {
  internal_ip_address = openstack_compute_instance_v2.irefindex.access_ip_v4
  internal_port_id    = openstack_networking_port_v2.irefindex.id
  floatingip_id       = var.floating_ip_id
  external_port       = var.ssh_port
  internal_port       = 22
  protocol            = "tcp"

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y python3-pip",
      "sudo pip3 install --upgrade pip",
      "sudo pip3 install ansible"
    ]

    connection {
      host        = var.floating_ip
      port = var.ssh_port
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.private_key_path)
    }
  }

  provisioner "local-exec" {
    // StrictHostKeyChecking is set to no as when running this multiple times (e.g. after a terraform destroy), the host key will change and this would fail.
    command = "ansible-playbook -i '${var.floating_ip},' --ssh-extra-args '-p ${var.ssh_port} -o StrictHostKeyChecking=no' -u ${var.ssh_user} --private-key '${var.private_key_path}' ../ansible/hello-world.yml"
  }
}

