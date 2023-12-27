FROM debian:bullseye

# Install sudo
RUN apt-get update && apt-get install -y sudo ansible

# Create a non-root user with sudo privileges
RUN useradd -m ansible_user && \
    echo "ansible_user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ansible_user

# Switch to the non-root user
USER ansible_user

# Set the working directory
WORKDIR /ansible

# Copy your Ansible playbook and files
COPY vsc/ansible/ .
COPY oci/inventory.ini .

# We can already build the structure for the container
RUN ansible-playbook -i inventory.ini irinit.yml

# Clean up APT when done to reduce image size
USER root
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Switch back to the non-root user
USER ansible_user

# Run all other scripts
COPY oci/run_in_container.bash .
CMD ["/bin/bash", "/ansible/run_in_container.bash"]
