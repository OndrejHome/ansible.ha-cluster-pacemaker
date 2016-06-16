#!/usr/bin/python

DOCUMENTATION = '''
---
module: pcs_resource
short_description: PCS RESOURCE module
description:
     - module for handling resources (currenlty only stonith resources) in pacemaker cluster
version_added: "0.1"
options:
  name:
    description:
      - resource name
    required: true
    default: null
  stonith:
    description:
      - is this a stonith resource?
    required: true
    default: no
  resource_type:
    description:
      - resource type name
    required: true
    default: null
  options:
    description:
      - pcs resource create options
    required: false
    default: null
notes:
   - ALPHA QUALITY: Not tested extensively
   - provides only creation and detection of presence, no advanced features
   - tested on RHEL+CentOS 6.8 and 7.2
requirements: [ ]
author: "Ondrej Famera <ondrej-xa2iel8u@famera.cz>"
'''

EXAMPLES = '''
# create stonith devices, for each node one with fence_xvm and with name of node on hypervisor stored in hypervisor_name ansible inventory variable 
- pcs_resource: name="fence-{{ hostvars[item]['ansible_fqdn'].split('.')[0] }}" stonith=true resource_type=fence_xvm options="pcmk_host_map={{ hostvars[item]['ansible_fqdn'].split('.')[0] }}:{{ hostvars[item]['hypervisor_hostname'] }}; op monitor interval=30s"
  with_items: play_hosts
  run_once: true
'''

try:
    import pcs.utils
    HAVE_PCS=True
except ImportError:
    HAVE_PCS=False
    try:
        import sys
        sys.path.append("/usr/lib/python2.6/site-packages/pcs/")
        import pcs.utils
        import pcs.resource
        HAVE_PCS=True
    except ImportError:
        HAVE_PCS=False

def main():
        module = AnsibleModule(
                argument_spec = dict(
                        name=dict(required=True),
                        stonith=dict(default='no', type='bool'),
                        resource_type=dict(required=True),
                        options=dict(required=False),
                ),
                supports_check_mode=True
        )

        if not HAVE_PCS:
            module.fail_json(msg="This module requires pcs")

        name = module.params['name']
        stonith = module.params['stonith']
        resource_type = module.params['resource_type']
        options = module.params['options']

        result = {}
        result['name'] = name


        root = pcs.utils.get_cib_etree()
        resources = root.find(".//resources")

        resource_found = False
        for child in resources.findall(".//*"):
            if "id" in child.attrib and child.attrib["id"] == name and (stonith and pcs.utils.is_stonith_resource(name) or (not stonith and not pcs.utils.is_stonith_resource(name))):
                resource_found = True
                break

        if resource_found:
            result['state'] = resource_found
            result['changed'] = False
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            else: 
                # create resource
                st_values, op_values, meta_values = pcs.resource.parse_resource_options(
                    options.split(), with_clone=False
                )
                try:
                    resource_type_name = resource_type
                    if stonith:
                        resource_type_name = "stonith:"+resource_type
                    pcs.resource.resource_create(name,resource_type_name,st_values, op_values, meta_values)
                    result['changed'] = True
                except:
                    module.fail_json(msg="failed to create stonith device")
        module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
