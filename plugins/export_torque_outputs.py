#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
DOCUMENTATION = r'''
---
module: export_torque_outputs

short_description: Exports outputs to a .json file

version_added: "1.0.0"

description: This module allows collecting the playbook outputs and export them to a .json file, that Torque will use as the grain outputs.

options:
    outputs:
        required: true
        type: dict

author:
    - Torque
'''

EXAMPLES = r'''
- name: Export outputs
  torque.collections.export_torque_outputs:
    outputs: 
      output1: "{{ result }}
'''
import json
from ansible.module_utils.basic import AnsibleModule

def export_torque_outputs(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def main():
    module_args = dict(
        outputs=dict(type='dict', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    outputs = module.params['outputs']

    export_torque_outputs(outputs, "torque-outputs.json")

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
