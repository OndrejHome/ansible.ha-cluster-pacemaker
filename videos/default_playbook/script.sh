#!/bin/bash
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
echo "[user@examples ~]$ ansible-galaxy install OndrejHome.ha-cluster-pacemaker -p roles"
ansible-galaxy install OndrejHome.ha-cluster-pacemaker -p roles
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
