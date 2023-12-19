#!/bin/bash

# Default env file path
DEFAULT_ENV_FILE="./terraform/irefindex.auto.tfvars"

# Function to display usage
usage() {
  echo "Usage: $0 [env_file]"
}

# Function to check if a file exists
file_exists() {
  local file="$1"
  [ -f "$file" ]
}

# Function to read and parse the env file
read_env_file() {
  local env_file="$1"

  while IFS='=' read -r key value; do
    key=$(echo "$key" | tr -d '[:space:]')
    value=$(echo "$value" | tr -d '[:space:]' | sed 's/^"\|"$//g')

    case $key in
      "ssh_port") ssh_port="$value" ;;
      "floating_ip") floating_ip="$value" ;;
    esac
  done < "$env_file"
}

# Function to remove SSH host key entry
remove_ssh_host_key() {
  local host="[${floating_ip}]:${ssh_port}"
  ssh-keygen -R "$host"
  echo "SSH host key entry removed for $host"
}

# Default env file path
env_file=${1:-$DEFAULT_ENV_FILE}

# Check if the provided or default env file exists
if ! file_exists "$env_file"; then
  echo "Error: Env file not found: $env_file"
  usage
  exit 1
fi

# Read and parse the env file
read_env_file "$env_file"

# Check if required variables are set
if [ -z "$ssh_port" ] || [ -z "$floating_ip" ]; then
  echo "Error: Missing required information in the env file."
  usage
  exit 1
fi

# Remove the SSH host key entry
remove_ssh_host_key
