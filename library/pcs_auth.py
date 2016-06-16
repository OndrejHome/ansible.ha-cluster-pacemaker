#!/usr/bin/python

DOCUMENTATION = '''
---
module: pcs_auth
short_description: PCS AUTH module for pacemaker clusters
description:
     - module for handling authorizations in pacemaker clusters based on 'pcs auth' logic
version_added: "0.1"
options:
  fqdn:
    description:
      - FQDN of cluster node
    required: true
    default: null
  username:
    description:
      - cluster username
    required: true
    default: null
  password:
    description:
      - cluster password
    required: true
    default: null
notes:
   - ALPHA QUALITY: Not tested extensively
   - provides only creation and detection of presence, no advanced features
   - tested on RHEL+CentOS 6.8 and 7.2
requirements: [ ]
author: "Ondrej Famera <ondrej-xa2iel8u@famera.cz>"
'''

EXAMPLES = '''
# Authorize all nodes in ansible play using their first part of hostname as FQDN (this part must be resolvable or available in /etc/hosts)
- pcs_auth: fqdn={{ hostvars[item]['ansible_fqdn'].split('.')[0] }} username={{ cluster_user }} password={{ cluster_user_pass }}
  run_once: true
  with_items: play_hosts
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
        HAVE_PCS=True
    except ImportError:
        HAVE_PCS=False

def main():
        module = AnsibleModule(
                argument_spec = dict(
                        fqdn=dict(required=True),
                        username=dict(required=True),
                        password=dict(required=True),
                ),
                supports_check_mode=True
        )

        if not HAVE_PCS:
            module.fail_json(msg="This module requires pcs")

        fqdn = module.params['fqdn']
        username = module.params['username']
        password = module.params['password']

        result = {}
        result['fqdn'] = fqdn

        # hacks for centos/rhel 7
        sys.argv[0]="/usr/lib/pcsd/" #FIXME pcs.utils.run_pcsdcli function doesn't work well without this
        os.environ['CIB_user'] = username

        status = pcs.utils.checkAuthorization(fqdn)
        if status[0] == 0:
            try:
                auth_status = json.loads(status[1])
                if auth_status["success"]:
                # FIXME - this need to be checked with cluster.py to be complete
                    result['state'] = status[0]
                    result['changed'] = False
            except:
                pass
        elif status[0] == 3:
            if module.check_mode:
                module.exit_json(changed=True)
            else:
                output = {}
                output['status'] = ''
                try:
                    retval = pcs.utils.updateToken(fqdn,fqdn,username,password)
                except:
                    pcsd_data = {
                        'nodes': [ fqdn ],
                        'username': username,
                        'password': password
                    }
                    output, retval = pcs.utils.run_pcsdcli('auth', pcsd_data)
                if (retval and output['status'] == 'ok' ) or output['status'] == 'access_denied':
                    module.fail_json(msg="Failed authorizing node - %s , %s" %(retval, output['status']) )
                else:
                    result['changed']=True
        else:
            module.fail_json(msg="Failed authorizing node %s - %s" %(fqdn, status) )
        module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
