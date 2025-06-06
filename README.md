ha-cluster-pacemaker
=========

Role for configuring and expanding basic pacemaker cluster on CentOS/RHEL 6/7/8/9, AlmaLinux 8/9, Rocky Linux 8/9, Fedora 31/32/33/34/35/36/37/38/39/40/41/42 and CentOS 8/9 Stream systems. Initial support for CentOS 10 Stream and AlmaLinux 10 Beta.

This role can configure following aspects of pacemaker cluster:
- enable needed system repositories
- install needed packages
- create and configure users and groups for running pacemaker cluster
- configure firewall
- generate items in `/etc/hosts`
- authorize cluster nodes
- create cluster or expand cluster (check `allow_cluster_expansion`)
  - "2 or more" node cluster
  - single heartbeat, rrp or knet with up to 8 links
  - remote nodes
  - use autodetected or custom selected interfaces/IPs for heartbeat
- start and enable cluster on boot
- configure stonith devices
  - by default install and configure `fence_xvm` stonith devices
  - optionally configure `fence_kdump`
  - optionally configure `fence_vmware` (SOAP/REST) or any other `fence_*` stonith devices
  - optionally configure `fence_aws`

Role fully supports `--check` mode for default configuration and partially supports it for most of other options.

When reporting issue please provide following information (if possible):
- used ansible version
- OS from which ansible was run
- playbook and invetory file that produced error (remove sensitive information where appropriate)
- error message or description of missbehaviour that you have encountered

Requirements
------------

This role depend on role [ondrejhome.pcs-modules-2](https://github.com/OndrejHome/ansible.pcs-modules-2).

**Ansible 2.8** or later. (NOTE: it might be possible to use earlier versions, in case of issues please try updating Ansible to 2.8+)

**RHEL 6/7/8:** It is expected that machines will already be registered. Role will by default enable access to 'High Availability' or 'Resilient storage' channel. If this is not desired check the `enable_repos` variable.

**RHEL/CentOS 7:** This role requires at least version `2.9` of `python-jinja2` library. If not present you may encounter error described in Issue #6. To get the updated version of `python-jinja2` and its dependencies you can use following RPM repository - https://copr.fedorainfracloud.org/coprs/ondrejhome/ansible-deps-el7/ for both CentOS 7 and RHEL 7.

**CentOS 8 Stream** Tested with version 20240129 minimal recommended ansible version is **2.11.0** which starts to identify system as 'CentOS' instead of 'RedHat' (unline CentOS Linux). The older CentOS 8 Stream versions 20201211 minimal usable ansible version is **2.9.16/2.10.4**. Version **2.8.18** was **not** working at time of testing. This is related to [Service is in unknown state #71528](https://github.com/ansible/ansible/issues/71528).

**CentOS 9 Stream** Tested with version 20240129 minimal recommended ansible is **2.11.0**.

**Debian Buster** Tested with version 20210310 with ansible version **2.10** and **Debian Bullseye** Tested with version 20220326 with ansible version **2.12**. Debian part of this role does not include the stonith configuration and the firewall configuration. **Note:** This role went only through limited testing on Debian - not all features of this role were tested.

**Debian Bookworm** Tested with ansible version **2.14** and **Debian Bookwork**. Debian part of this role does not include the stonith configuration and the firewall configuration. **Note:** This role went only through limited testing on Debian - not all features of this role were tested.

Ansible version **2.9.10** and **2.9.11** will fail with error `"'hostvars' is undefined"` when trying to configure remote nodes. This applies only when there is at least one node with `cluster_node_is_remote=True`. **Avoid these Ansible versions** if you plan to configure remote nodes with this role.

On **CentOS Linux 8** you have to ensure that BaseOS and Appstream repositories are working properly. As the CentOS Linux 8 is in the End-Of-Life phase, this role will configure HA repository to point to vault.centos.org if repository configuration (`enable_repos: true`) is requested (it is by default).

When using **Fedora 41/42** with minimal installation then this role will automatically install `python3-libdnf5` package to allow regular ansible yum module to function.

**pcs-0.11** version distributions (AlmaLinux 9, Rocky Linux 9, RHEL 9, Fedora 36/37/38) are supported only with ondrejhome.pcs-modules-2 version 27.0.0 or higher.

**pcs-0.12** version distributions (AlmaLinux 10, CentOS Stream 10, Fedora 42) are supported only with ondrejhome.pcs-modules-2 version 31.0.0 or higher.

Role Variables
--------------

  - user used for authorizing cluster nodes

    ```
    cluster_user: 'hacluster'
    ```

  - password for user used for authorizing cluster nodes

    ```
    cluster_user_pass: 'testtest'
    ```

  - group to which cluster user belongs (should be 'haclient')

    ```
    cluster_group: 'haclient'
    ```

  - name of the cluster

    ```
    cluster_name: 'pacemaker'
    ```

  - configuration of firewall for clustering, NOTE in RHEL/Centos 6 this replaces iptables configuration file!

    ```
    cluster_firewall: true
    ```

  - enable cluster on boot on normal (not pacemaker_remote) nodes

    ```
    cluster_enable_service: true
    ```

  - configure cluster with fence_xvm fencing device ?
    This will copy /etc/cluster/fence_xvm.key to nodes and add fencing devices to cluster
    NOTE: you need to define 'vm_name' in the inventory for each cluster node

    ```
    cluster_configure_fence_xvm: true
    ```

  - configure cluster with fence_vmware_soap/fence_vmware_rest fencing device ?
    This will install fence_vmware_soap/fence_vmware_rest fencing agent and configure it. When this is enabled you
    have to specify 3 additional variables with information on accessing the vCenter.
    NOTE: You also need to define 'vm_name' in the inventory for each cluster node specifying the name or UUID of VM
    as seen on the hypervisor or in the output of `fence_vmware_soap -o list`/`fence_vmware_rest` command.
    ```
    cluster_configure_fence_vmware_soap: false
    cluster_configure_fence_vmware_rest: false
    fence_vmware_ipaddr: ''
    fence_vmware_login: ''
    fence_vmware_passwd: ''
    ```
    You can optionally change the additional attributes passed to fence_vmware_soap/fence_vmware_rest using the variable `fence_vmware_options`.
    By default this variable enables encryption but disables validation of certificates.
    ```
    fence_vmware_options: 'ssl="1" ssl_insecure="1"'
    ```
    NOTE: Only one of fence_vmware_soap/fence_vmware_rest can be configured as stonith devices share same name.

  - configure cluster with fence_kdump fencing device ?
    This starts kdump service and defines the fence_kdump stonith devices.
    NOTE: if the kdump service is not started this won't work properly or at all

    ```
    cluster_configure_fence_kdump: false
    ```

  - configure cluster with fence_aws fencing device?
    You must provide instance id/region of AWS and Instance Profile that is able to start/stop instances for this cluster.
    When this is enabled you have to specify `fence_aws_region` variable with information on AWS region.
    NOTE: If you don't set up instance profile, it won't work properly or at all

    ```
    cluster_configure_fence_aws: false
    fence_aws_region: ''
    ```
    NOTE: You also need to define `instance_id` in the inventory for each cluster node by specifying the instance id
    as seen in the AWS web console or in the output of `fence_aws -o list` command. ([man fence_aws](https://www.mankier.com/8/fence_aws))

    You can optionally change the additional attributes passed to fence_aws using the `fence_aws_options` variable.
    ```
    fence_aws_options: ''
    ``` 
    NOTE: Examples of proper options for some specific use cases can be found in documents below.   
    [https://access.redhat.com/articles/4175371#create-stonith](https://access.redhat.com/articles/4175371#create-stonith)   
    [https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-cluster-resources-1.html](https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-cluster-resources-1.html)    

  - How to map fence devices to cluster nodes?
    By default for every cluster node a separate stonith devices is created ('one-device-per-node').
    Some fence agents can fence multiple nodes using same stonith device ('one-device-per-cluster')
    and can have trouble when using multiple devices due to same user login count limits.
    Available options:
      - `one-device-per-node` - (default) - one stonith device per cluster node is created
      - `one-device-per-cluster` - (on supported fence agents) - only one cluster-wide stonith device is created for all nodes, supported fence agents: `fence_vmware_rest`, `fence_vmware_soap`, `fence_xvm`, `fence_kdump`
    ```
    cluster_configure_stonith_style: 'one-device-per-node'
    ```

  - (RHEL/CentOS/AlmaLinux/Rocky) enable the repositories containing needed packages
    ```
    enable_repos: true
    ```

  - (RHEL only) enable the extended update (EUS) repositories containint packages needed
    ```
    enable_eus_repos: false
    ```

  - (RHEL only) enable the SAP Solutions update service (E4S) repositories containint packages needed
    ```
    enable_e4s_repos: false
    ```

  - (RHEL only) enable Beta repositories containint packages needed
    ```
    enable_beta_repos: false
    ```

  - (RHEL only) type of enable repositories, note that E4S repos have only 'ha' type available
    - ha - High-Availability
    - rs - Resilient Storage
    ```
    repos_type: 'ha'
    ```

  - (RHEL only) custom_repository allows enabling an arbitrarily named repository to be enabled.
    RHEL8 repo names can be found at http://downloads.redhat.com/redhat/rhel/rhel-8-beta/rhel-8-beta.repo
    ```
    custom_repository: ''

    ```

  - (CentOS only) install the needed packages from the CD-ROM media available at /dev/cdrom
    ```
    use_local_media: false
    ```

  - Enable or disable PCSD web GUI. By default the role keeps the default of installation means that
    PCSD web GUI is disabled on CentOS/RHEL 6.X and enabled on CentOS/RHEL 7.X. `true` or `false` can
    be passed to this variable to make sure that PCSD web GUI is enabled or disabled.
    ```
    enable_pcsd_gui: 'nochange'
    ```

  - Cluster transport protocol. By default this role will use what is default for give OS.
    For CentOS/RHEL 6.X this means 'udp' (UDP multicast) and for CentOS/RHEL 7.X this means 'udpu'
    (UDP unicast). This variable accepts following options: `default`, `udp` and `udpu`.
    ```
    cluster_transport: 'default'
    ```

  - Allow adding nodes to existing cluster when used with ondrejhome.pcs-modules-2 v16 or newer.
    ```
    allow_cluster_expansion: false
    ```

  - Cluster network interface. If specified the role will map hosts to primary IPv4 address from this interface.
    By default the IPv4 address from `ansible_default_ipv4` or first IPv4 from `ansible_all_ipv4_addresses`is used.
    For exmaple to use primary IPv4 address from interface `ens8` use `cluster_net_iface: 'ens8'`.
    Interface must exists on all cluster nodes.
    ```
    cluster_net_iface: ''
    ```

  - Redundant network interface. If specified the role will setup a corosync redundant ring using the default IPv4 from this interface.
    Interface must exist on all cluster nodes.
    ```
      rrp_interface: ''
    ```
    NOTE: you can define this variable either in defaults/main.yml, in this case the same rrp_interface name is used for all hosts in the hosts file.
          Either you specify an interface for each host present in the hosts file: this allows to use a specific interface name for each host (in the case they dont have the same interface name). Also note that instead of defining rrp_interface for a host, you can define rrp_ip: in this case this alternate ip is used to configure corosync RRP (this IP must be different than the host' default IPv4 address). This allows to use an alternate ip belonging to the same primary interface.


  - Whether to add hosts to /etc/hosts. By default an entry for the hostname
    given by `cluster_hostname_fact` is added for each host to `/etc/hosts`.
    This can be disabled by setting `cluster_etc_hosts` to `false`.

    ```
    cluster_etc_hosts: true
    ```

  - Which Ansible fact to use as the hostname of cluster nodes. By default this
    role uses the `ansible_hostname` fact as the hostname for each host. In
    some environments it may be useful to use the Fully Qualified Domain Name
    (FQDN) `ansible_fqdn` or node name `ansible_nodename`.

    ```
    cluster_hostname_fact: "ansible_hostname"
    ```

  - Whether the node should be setup as a remote pacemaker node. By default
    this is `false`, and the node will be a full member of the Pacemaker
    cluster.  Pacemaker remote nodes are not full members of the cluster, and
    allow exceeding the maximum cluster size of 32 full members. Note that
    remote nodes are supported by this role only on EL7 and EL8.

    ```
    cluster_node_is_remote: false
    ```

  - Ordered list of variables for detecting primary cluster IP (ring0). First matched IPv4 is used and rest
    of detected IPv4s are skipped. In majority cases this should not require change, in some special cases
    such as when there is no default GW or non-primary IPv4 from given interface should be used this can be adjusted.
    ```
    ring0_ip_ordered_detection_list:
      - "{{ hostvars[inventory_hostname]['ansible_'+cluster_net_iface].ipv4.address|default('') }}"
      - "{{ ansible_default_ipv4.address|default('') }}"
      - "{{ ansible_all_ipv4_addresses[0]|default('') }}"

    ```

  - Configure cluster properties (Not mandatory)

    ```
    cluster_property:
      - name: required
        node: optional
        value: optional
    ```

  - Configure cluster resource defaults (Not mandatory)

    ```
    cluster_resource_defaults:
      - name: required
        defaults_type: optional
        value: optional
    ```

  - Configure cluster resources (Not mandatory)

    ```
    cluster_resource:
      - name: required
        resource_class: optional
        resource_type: optional
        options: optional
        force_resource_update: optional
        ignored_meta_attributes: optional
        child_name: optional
    ```

  - Configure cluster order constraints (Not mandatory)

    ```
    cluster_constraint_order:
      - resource1: required
        resource1_action: optional
        resource2: required
        resource2_action: optional
        kind: optional
        symmetrical: optional
    ```
  - Configure cluster colocation constraints (Not mandatory)

    ```
    cluster_constraint_colocation:
      - resource1: required
        resource1_role: optional
        resource2: required
        resource2_role: optional
        score: optional
        influence: optional
    ```

  - Configure cluster location constraints (Not mandatory)

    **node based**

    ```
    cluster_constraint_location:
      - resource: required
        node_name: required
        score: optional
    ```

    **rule based** (_needs ondrejhome.pcs-modules-2 version 30.0.0 or newer_)

    ```
    cluster_constraint_location:
      - resource: required
        constraint_id: required
        rule: required
        score: optional
    ```

Security considerations
-----------------------

Please consider updating the default value for `cluster_user_pass`.

To protect the sensitive values in variables passed to this role you can use `ansible-vault` to encrypt them. The recommended approach is to create a separate file with desired variables and their values, encrypt the whole file with `ansible-vault encrypt` and then include this file in `pre_tasks:` section so it is loaded before the role is executed. Example below illustrates this whole process.

**Creating encrypted_vars.yaml file**

- 1. Create plain text `encrypted_vars.yaml` file with your desired secret values
    ```
    # cat encrypted_vars.yaml
    ---
    cluster_user_pass: 'cluster-user-pass'
    fence_vmware_login: 'vcenter-user'
    fence_vmware_passwd: 'vcenter-pass'
    ```

- 2. Encrypt file suing `ansible-vault`
    ```
    # ansible-vault encrypt encrypted_vars.yaml
    ```

- 3. Verify the new content of `encrypted_vars.yaml`
    ```
    # cat encrypted_vars.yaml
    $ANSIBLE_VAULT;1.1;AES256
    31306461386430...
    ```

**Example playbook that is using values from `encrypted_vars.yaml`**

    - hosts: cluster
       pre_tasks:
         - include_vars: encrypted_vars.yaml
       roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'test-cluster' }

**NOTE:** Encrypting only the variable's value and putting it into `vars:` is discouraged as it could results in errors like `argument 1 must be str, not AnsibleVaultEncryptedUnicode`. Approach that encrypts whole file seems to be not affected by this issue.

Ansible module_defaults
-----------------------

While this role does not expose all configuration options through variables, one can use the [`module_defaults`](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html#module-defaults) to change the default values of parameters that this role does not use. Below is non-exhaustive list of examples where this may become useful.

**Example module_default A** for setting the totem token to 15 seconds

    - hosts: cluster
      modules_defaults:
        pcs_cluster:
          token: 15000               # default is 'null' - depends on OS default value

**Example module_default B** for disabling installation of weak dependencies on EL8+/Fedora systems

    - hosts: cluster
      modules_defaults:
        yum:
          install_weak_deps: false   # default is 'true'

**Example module_default C** for disabling installation of package recommends on Debian systems

    - hosts: cluster
      modules_defaults:
        apt:
          install_recommends: false  # default is 'null' - depends on OS configuration

NOTE: The `module_defaults` only applies to options that are not specified in task - you cannot override value that is set by task in this role, only the value of options that are not used can be changed.

Example Playbook
----------------

**Example playbook A** for creating cluster named 'test-cluster' enabled on boot, with `fence_xvm` and firewall settings. NOTE: `cluster_name` is optional and defaults to `pacemaker`.

    - hosts: cluster
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'test-cluster' }

**Example playbook B** for creating cluster named 'test-cluster' without configuring firewall and without `fence_xvm`.
For cluster to get properly authorized it is expected that firewall is already configured or disabled.

    - hosts: cluster
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'test-cluster', cluster_firewall: false, cluster_configure_fence_xvm: false }

**Example playbook C** for creating cluster named `vmware-cluster` with `fence_vmware_soap` fencing device.

    - hosts: cluster
      vars:
        fence_vmware_ipaddr: 'vcenter-hostname-or-ip'
        fence_vmware_login: 'vcenter-username'
        fence_vmware_passwd: 'vcenter-password-for-username'
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'vmware-cluster', cluster_configure_fence_xvm: false, cluster_configure_fence_vmware_soap: true }

**Example playbook D** for creating cluster named `test-cluster` where `/etc/hosts` is not modified:

    - hosts: cluster
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'test-cluster', cluster_etc_hosts: false }

**Example playbook E** for creating cluster named `vmware-cluster` with single `fence_vmware_rest` fencing device for all cluster nodes.

    - hosts: cluster
      vars:
        fence_vmware_ipaddr: 'vcenter-hostname-or-ip'
        fence_vmware_login: 'vcenter-username'
        fence_vmware_passwd: 'vcenter-password-for-username'
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'vmware-cluster', cluster_configure_fence_xvm: false, cluster_configure_fence_vmware_rest: true, cluster_configure_stonith_style: 'one-device-per-cluster' }

**Example playbook F** for creating cluster named `aws-cluster` with single `fence_aws` fencing device for all cluster nodes.

    - hosts: cluster
      roles:
        - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'aws-cluster', cluster_configure_fence_xvm: false, cluster_configure_fence_aws: true, cluster_configure_stonith_style: 'one-device-per-cluster', enable_repos: false, fence_aws_region: 'aws-region' }

**Example playbook Resources configuration** .

    - hosts: cluster
      vars:
        cluster_property:
          - name: 'maintenance-mode'
            value: 'true'
        cluster_resource:
          - name: 'apache2'
            resource_type: 'systemd:apache2'
            options: 'meta migration-threshold=2 op monitor interval=20s timeout=10s'
          - name: 'cluster_vip'
            resource_type: 'ocf:heartbeat:IPaddr2'
            options: 'ip=192.168.1.150 cidr_netmask=24 meta migration-threshold=2 op monitor interval=20'
        cluster_constraint_colocation:
          - resource1: 'cluster_vip'
            resource2: 'apache2'
            score: 'INFINITY'
        cluster_resource_defaults:
          - name: 'failure-timeout'
            value: '30'
      roles:
         - { role: 'ondrejhome.ha-cluster-pacemaker', cluster_name: 'apache-cluster'}

Inventory file example for CentOS/RHEL/Fedora systems createing basic clusters.

    [cluster-centos7]
    192.168.22.21 vm_name=fastvm-centos-7.8-21
    192.168.22.22 vm_name=fastvm-centos-7.8-22
    [cluster-fedora32]
    192.168.22.23 vm_name=fastvm-fedora32-23
    192.168.22.24 vm_name=fastvm-fedora32-24
    [cluster-rhel8]
    192.168.22.25 vm_name=fastvm-rhel-8.0-25
    192.168.22.26 vm_name=fastvm-rhel-8.0-26

Inventory file example for cluster using RRP interconnnect on custom interface and/or using custom IP for RRP

    [cluster-centos7-rrp]
    192.168.22.27 vm_name=fastvm-centos-7.6-21 rrp_interface=ens6
    192.168.22.28 vm_name=fastvm-centos-7.6-22 rrp_ip=192.168.22.29

Inventory file example with two full members and two remote nodes:

    [cluster]
    192.168.22.21 vm_name=fastvm-centos-7.6-21
    192.168.22.22 vm_name=fastvm-centos-7.6-22
    192.168.22.23 vm_name=fastvm-centos-7.6-23 cluster_node_is_remote=True
    192.168.22.24 vm_name=fastvm-centos-7.6-24 cluster_node_is_remote=True

Inventory file example with fence_aws:

    [cluster]
    172.31.0.1	instance_id="i-acbdefg1234567890"
    172.31.0.2	instance_id="i-acbdefg0987654321"

Old video examples of running role with defaults for:
  - CentOS 7.6 installing CentOS 7.6 two node cluster: https://asciinema.org/a/226466
  - Fedora 29 installing Fedora 29 two node cluster: https://asciinema.org/a/226467

License
-------

GPLv3

Author Information
------------------

To get in touch with author you can use email ondrej-xa2iel8u@famera.cz or create a issue on github when requesting some feature.
