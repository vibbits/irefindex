FROM debian:bookworm

RUN apt-get update && apt-get install -y ansible

WORKDIR /ansible

COPY vsc/ansible/ .
COPY oci/inventory.ini .

# We can already build the structure for the container
RUN ansible-playbook -i inventory.ini irinit.yml

# Clean up APT when done to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Run all other scripts
COPY oci/run_in_container.bash .
CMD ["/bin/bash", "/ansible/run_in_container.bash"]
