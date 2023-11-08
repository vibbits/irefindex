variable "base_name" {
  type        = string
  description = "Base name for the instance"
}

variable "network_id" {
  type        = string
  description = "Network ID for the instance"
}

variable "image_name" {
  type        = string
  default     = "Debian-11"
  description = "Image name for the instance"
}

variable "flavor_name" {
  type        = string
  default     = "CPUv1.small"
  description = "Flavor name for the instance"

  validation {
    condition     = can(regex("^(CPU|GPU|UPS)v[0-9]+\\.(nano|tiny|small|medium|large|2xlarge|3xlarge|1_2xlarge|1_3xlarge|4xlarge)$", var.flavor_name))
    error_message = "Flavor name must be one of CPUv1.nano, CPUv1.tiny, GPUv2.small, CPUv1.small, GPUv3.small, UPSv1.small, UPSv1.medium, GPUv2.medium, GPUv3.medium, CPUv1.medium, UPSv1.large, GPUv2.large, GPUv3.large, CPUv1.large, CPUv1.xlarge, UPSv1.2xlarge, GPUv2.2xlarge, GPUv3.2xlarge, CPUv1.2xlarge, CPUv1.1_2xlarge, UPSv1.3xlarge, CPUv1.3xlarge, CPUv1.1_3xlarge, CPUv1.4xlarge"
  }
}

variable "network_name" {
  type        = string
  default     = "VSC_2021_102_vm"
  description = "Network name for the instance"
}

variable "floating_ip" {
  type        = string
  description = "Floating IP for the instance"
}

variable "floating_ip_id" {
  type        = string
  description = "Floating IP ID for the instance"
}

variable "ssh_port" {
  type        = number
  description = "SSH port for the instance (ideally in 50k range)"
}

variable "private_key_path" {
  type        = string
  description = "Private key path for the instance"
}

variable "ssh_user" {
  type        = string
  description = "SSH user for the instance"
}
