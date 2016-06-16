ha-cluster-pacemaker
=========

Role for configuring basic pacemaker cluster on CentOS/RHEL 6/7 systems.

Requirements
------------

RHEL: It is expected that machines will already be registered and subscribed for access to 'High Availability' or 'Resilient storage' channels.

Role Variables
--------------

  - user used for authorizing cluster nodes
  cluster_user: hacluster
  cluster_user_pass: testtest

  - group to which cluster user belongs (should be 'haclient')
  cluster_group: haclient

  - name of the cluster
  cluster_name: pacemaker

  - configuration of firewall for clustering, NOTE in RHEL/Centos 6 this replaces iptables configuration file!
  cluster_firewall: true

  - enable cluster on boot
  cluster_enable_service: true

  - configure cluster with fence_xvm fencing device ?
    This will copy /etc/cluster/fence_xvm.key to nodes and add fencing devices to cluster
    NOTE: you need to define 'hypervisor_name' in the inventory for each cluster node
  cluster_configure_fence_xvm: true

Example Playbook
----------------

Example playbook for creating cluster named 'test1' enabled on boot, with fence_xvm and firewall settings

    - hosts: servers
      roles:
         - { role: OndrejHome.ha-cluster-pacemaker, cluster_name: 'test1' }

Example for creating cluster named 'test2' without configuring firewalling and without fence_xvm.
For cluster to get properly authorize it is expected that firewall is already configured or disabled.

    - hosts: servers
      roles:
         - { role: OndrejHome.ha-cluster-pacemaker, cluster_name: 'test2', cluster_firewall: false, cluster_configure_fence_xvm: false }

License
-------

GPLv3

Author Information
------------------

WARNING: this is alpha-version quality proof-of concept role that still needs some polishing and is using custom modules 
         to interact with pacemaker through python. This is suitable for testing purposes only.

To get in touch with author you can use email ondrej-xa2iel8u@famera.cz or create a issue on github when requesting some feature.
