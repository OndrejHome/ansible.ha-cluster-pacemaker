#!/bin/bash
export ANSIBLE_FORCE_COLOR=true
##
echo "[user@examples ~]$ cat /etc/redhat-release"
cat /etc/redhat-release
sleep 1

##
echo "[user@examples ~]$ ansible --version"
ansible --version
sleep 1

##
echo "[user@examples ~]$ cat our_environment"
cat our_environment
sleep 4

##
echo "[user@examples ~]$ ls -l /etc/cluster/fence_xvm.key"
ls -l /etc/cluster/fence_xvm.key
sleep 2

##
echo "[user@examples ~]$ ansible-galaxy install ondrejhome.ha-cluster-pacemaker,19.0.0 ondrejhome.pcs-modules-2,19.0.0 -p roles"
ansible-galaxy install ondrejhome.ha-cluster-pacemaker,19.0.0 ondrejhome.pcs-modules-2,19.0.0 -p roles
sleep 2

##
echo "[user@examples ~]$ cat hosts-default"
cat hosts-default
sleep 2

## 
echo "[user@examples ~]$ cat playbook-default.yml"
cat playbook-default.yml
sleep 2

##
echo "[user@examples ~]$ ansible-playbook -i hosts-default playbook-default.yml"
ansible-playbook -i hosts-default playbook-default.yml
sleep 2
