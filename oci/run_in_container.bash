# !/bin/bash
#
# Everything in this script will be run in the container itself once the container has started.

# Run playbooks sequentially in localhost container.
run_playbooks(){
  for playbook in "$@"; do
    ansible-playbook -i inventory.ini $playbook.yml
  done
}

run_playbooks main1 main2 main3
