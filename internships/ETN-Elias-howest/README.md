To get started:
Start of with forking the github of iRefIndex from VIB. (https://github.com/vibbits/irefindex.git)
Ask a supervisor to set up a google cloud instance on a remote server. 
To connect with the server you will need the command:
```bash
ssh <username>@<ip-adress of the google cloud> -i id_ed25519
an example of this is the following:
ssh elias.steyaert@35.240.84.94 -i id_ed25519 
the id_ed25519 should be found in the ~/.ssh/ folder, if not, it can be added with the command: ssh-add ~/.ssh/id_ed25519
```
When the server is fully set up, the next thing should be to mount the "/dev/sda/" disk. 
To do this, follow the documentation here: https://cloud.google.com/compute/docs/disks/format-mount-disk-linux
It is HIGHLY RECOMMENDED if the "/dev/sda" disk is mounted with "/mnt/disks/data". That way the variables linked to this disk won't have to be changed.
This is easily done if you follow the documentation and replace "MOUNT_DIR" with "data".

Go into the directory: /irefindex/vsc and make a text file called "inventory"
In this text file, you paste the ip adress of the google cloud server.
in this same directory, you should also make an "ansible.cfg" file. This file should have:
```bash
[defaults]
remote_tmp = /mnt/disks/data
async_dir = /mnt/disks/data/.ansible_async
```

When these things are done, you can start the first playbook. This is done by going into the directory: /irefindex/vsc and performing the following command 
```bash
ansible-playbook -i inventory -u '<username>' --private-key=~/.ssh/id_ed25519 ansible/main1.yml
in my case this looked like this:
guest@fedora:~/internship/stage-VIB-irefindex/vsc]$ ansible-playbook -i inventory -u 'elias.steyaert' --private-key=~/.ssh/id_ed25519 ansible/after_main1.yml
(I forked the irefindex github into the directory "internship" and I changed the name of the irefindex directory to "stage-VIB-irefindex)
```

