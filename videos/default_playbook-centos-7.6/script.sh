#!/bin/bash
export ANSIBLE_FORCE_COLOR=true
##
echo "!! python-jinja2 package in CentOS/RHEL is very old and has some incopatibilities."
echo "Newer version is required when running plaubook from CentOS/RHEL machine !!"
echo "You can use steps below as root to get newer version of python-jinja2 package."
echo ""
##
echo "[root@examples ~]# curl https://copr.fedorainfracloud.org/coprs/ondrejhome/ansible-deps-el7/repo/epel-7/ondrejhome-ansible-deps-el7-epel-7.repo > /etc/yum.repos.d/ondrejhome-ansible-deps-el7-epel-7.repo"
echo "[root@examples ~]# yum update python-jinja2 python-markupsafe"
echo ""
sleep 10
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
