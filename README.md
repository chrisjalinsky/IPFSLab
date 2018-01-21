# Overview of IPFS Lab
The deploy script will configure a 3 node Ubuntu 16 IPFS private network. The goal is to keep all IPFS functionality initially contained within a private subnet.

For example, you want to run a private distributed application. At a future date, you open it up to public, by exposing the gateways and adding peers.

**Hosts:**
* ipfs1.lan
* ipfs2.lan
* ipfs3.lan

Additional blockchain tools and projects will be installed alongside the IPFS project including:
* [IPFS Peerpad](https://github.com/ipfs-shipyard/peerpad) - Awesome shared realtime NodeJS app utilizing ipfs.
* [IPFS WebUI](https://github.com/ipfs-shipyard/ipfs-webui) - Awesome frontend NodeJS app for ipfs.
* [Ethereum](https://ethereum.org/)
* [Rust](https://www.rust-lang.org/en-US/install.html) - Used for extracting ZIM archives, which we we import wikipedia to our local IPFS

### REQUIRED SOFTWARE

The development of this project was created on a Mac OSX (v10.12.6 Sierra) 16 GB laptop:


**The following applications are required for development**

* [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Ansible >= 2.4](http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-via-pip)

**Optional**

* [Vagrant Hostsupdater plugin](https://github.com/cogitatio/vagrant-hostsupdater) Install with: ```vagrant plugin install vagrant-hostsupdater``` This convenient but optional plugin is used to manage the ```/etc/hosts``` file on the hypervisor for accessing UIs and DNS.

### Install IPFSLab:

Simply clone the repo and run all commands from the root directory
```
git clone
cd IPFSLab
./ansible/scripts/deploy.sh
```

### Vagrant
Uses the box ```bento/ubuntu-16.04``` by default. This could be any flavor of Ubuntu 16.04

### Ansible
The deploy script runs the following playbook with a psuedo-dynamic inventory:
```
cd ansible
ansible-playbook deploy_environment.yaml -i inventory.py
```

#### ipfs_swarm_keygen role
Installs go library for creating a private swarm key. Additionally installs Nginx to expose the key. This should be shared more securely, but not for this lab exercise.

Additionally, the role creates a secure nginx server for the NodeJS apps.

#### ipfs_facts role
Creates custom ansible fact for ipfs on the remote nodes, by reading the JSON created by ipfs. View the fact:
```
ansible all -m setup -a 'filter=ansible_local' -i inventory.py
```

#### ipfs_webui role
[IPFS WebUI](https://github.com/ipfs-shipyard/ipfs-webui) - Awesome frontend NodeJS app for ipfs.

#### ipfs_peerpad role
[IPFS Peerpad](https://github.com/ipfs-shipyard/peerpad) - Awesome shared realtime NodeJS app utilizing ipfs.

The default install creates a NodeJS app which connects to the public IPFS swarm. This role rewrites the source code to connect to the private swarm.

The web address to connect to the WebUIs:
```
http://ipfs1.lan/
http://ipfs2.lan/
http://ipfs3.lan/
```

## Additional Details

### Private IPFS network
* For additional commands, see ```roles/ipfs/tasks/main.yml```
* [Experimental Features - Private Networks](https://github.com/ipfs/go-ipfs/blob/master/docs/experimental-features.md#private-networks)
* [Web UI from remote nodes](https://discuss.ipfs.io/t/running-ipfs-in-a-vm-with-webui/495/3)

**Much appreciation for the hard work and effort by these IPFS and Ethereum project's developers**
