# IPFS Ansible Vagrant

## GETTING STARTED

* When in doubt, ```vagrant destroy```. These VMs are meant to be ephemeral. If a provision doesn't succeed, just destroy and recreate. The purpose of this repo is to provide consistent environments and a repeatable automated procedure to build the infrastructure.

* Vagrant is utilized as a Virtualbox VM builder. The following dependencies are required to build the VMs locally.

### REQUIRED SOFTWARE

**The following applications are required**

* [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Ansible >= 2.4](http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-via-pip)

**Optional**

* [Vagrant Hostsupdater plugin](https://github.com/cogitatio/vagrant-hostsupdater) Install with: ```vagrant plugin install vagrant-hostsupdater``` This convenient but optional plugin is used to manage the ```/etc/hosts``` file on the hypervisor for accessing UIs and DNS.

### Install Lab:

Simply clone the repo and run all commands from the root directory
```
git clone
cd IPFSLab
./ansible/scripts/deploy.sh
```

### Vagrant and Ansible
Uses the box ```bento/ubuntu-16.04``` by default. This could be any favor of Ubuntu 16.04

### Private IPFS network
* For additional commands, see ```roles/ipfs/tasks/main.yml```
* [Experimental Features - Private Networks](https://github.com/ipfs/go-ipfs/blob/master/docs/experimental-features.md#private-networks)
