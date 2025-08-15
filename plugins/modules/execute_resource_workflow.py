#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: execute_resource_workflow

short_description: Execute a Torque workflow on a resource within an environment

version_added: "1.1.1"

description: 
    - This module allows executing workflows on resources within a Torque environment
    - Calls the Torque API endpoint to trigger workflows on specific resources

options:
    space:
        description:
            - The Torque space name
        required: true
        type: str
    environment:
        description:
            - The environment ID within the space
        required: true
        type: str
    grain_fullname:
        description:
            - The grain full name path
        required: true
        type: str
    resource:
        description:
            - The resource identifier within the grain
        required: true
        type: str
    workflow_name:
        description:
            - The workflow/blueprint name to execute
        required: true
        type: str
    repository_name:
        description:
            - The repository name containing the workflow
        required: true
        type: str
    inputs:
        description:
            - Key-value dictionary of inputs for the workflow
        required: false
        type: dict
        default: {}
    owner_email:
        description:
            - Email address of the workflow owner
        required: true
        type: str
    execution_name:
        description:
            - Custom execution name for the workflow
            - If not provided, will generate as "workflow_name__instantiation__{datetime}"
        required: false
        type: str
    api_token:
        description:
            - Torque API token for authentication
            - If not provided, will use TORQUE_API_TOKEN environment variable
        required: false
        type: str
    api_url:
        description:
            - Base URL for the Torque API
        required: false
        type: str
        default: "https://portal.qtorque.io"

author:
    - DBS
    - Torque
'''

EXAMPLES = r'''
- name: Execute workflow on vCenter VM
  torque.collections.execute_resource_workflow:
    space: 03-Live
    environment: Rr0LgPNF2j2C
    grain_fullname: vcenter-win2012-template
    resource: vsphere_virtual_machine.win-vm
    workflow_name: vcenter-vm-power-on
    repository_name: ProductionBPs
    owner_email: admin@example.com
    inputs:
      vm_name: "test-vm"
      cpu_count: 2
    api_token: "{{ torque_api_token }}"

- name: Execute workflow with custom execution name
  torque.collections.execute_resource_workflow:
    space: production
    environment: env_12345
    grain_fullname: web-server
    resource: aws_instance.web_1
    workflow_name: server-maintenance
    repository_name: MaintenanceBPs
    owner_email: devops@example.com
    execution_name: "custom-maintenance-task-001"
'''

RETURN = r'''
response:
    description: API response from the workflow execution
    returned: always
    type: dict
    sample: {
        "id": "workflow_12345",
        "status": "queued",
        "environment_name": "Power-on vCenter VM-TF-20250815T15023853",
        "blueprint_name": "vcenter-vm-power-on",
        "instantiation_name": "vcenter-vm-power-on__instantiation__20250814_212901_443"
    }
outputs:
    description: Workflow outputs if available in the response
    returned: when outputs are present in response
    type: dict
    sample: {
        "server_ip": "192.168.1.100",
        "status": "running"
    }
'''

import os
import json
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def generate_instantiation_name(workflow_name):
    """Generate execution name with current datetime"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Remove last 3 digits from microseconds
    return f"{workflow_name}__instantiation__{timestamp}"


def execute_resource_workflow(module, space, environment, grain_fullname, resource, workflow_name, 
                            repository_name, inputs, owner_email, execution_name, api_token, api_url):
    """Execute a Torque workflow via API call"""
    
    # Construct the API endpoint
    endpoint = f"/api/spaces/{space}/environments"
    url = f"{api_url.rstrip('/')}{endpoint}"
    
    # Generate instantiation name if not provided
    if not execution_name:
        execution_name = generate_instantiation_name(workflow_name)
    
    # Generate environment name
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")[:-2]  # Remove last 2 digits from microseconds
    environment_name = f"{workflow_name}-{timestamp}"
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Prepare request body
    body = {
        "environment_name": environment_name,
        "blueprint_name": workflow_name,
        "inputs": inputs,
        "source": {
            "repository_name": repository_name
        },
        "automation": "false",
        "owner_email": owner_email,
        "entity_metadata": {
            "type": "env_resource",
            "environment_id": environment,
            "grain_path": grain_fullname,
            "resource_id": resource
        },
        "env_references_values": {},
        "instantiation_name": execution_name
    }

    # Make the API call
    try:
        response, info = fetch_url(
            module=module,
            url=url,
            method='POST',
            headers=headers,
            data=json.dumps(body),
            timeout=30
        )
        
        # Check response status
        if info['status'] == 200 or info['status'] == 201 or info['status'] == 202:
            try:
                response_data = json.loads(response.read().decode('utf-8'))
                
                # Extract outputs if present
                outputs = response_data.get('outputs', {})
                
                return True, response_data, outputs, None
            except (ValueError, TypeError):
                return True, {"status": "success", "message": "Workflow executed successfully"}, {}, None
        else:
            error_msg = f"API call failed with status {info['status']} with message: {info.get('msg', '')}"
            try:
                error_body = response.read().decode('utf-8') if response else info.get('body', '')
                if error_body:
                    error_data = json.loads(error_body)
                    error_msg = error_data.get('message', error_msg)
            except:
                pass
            return False, None, {}, error_msg
            
    except Exception as e:
        return False, None, {}, f"Error making API call: {str(e)}"


def main():
    module_args = dict(
        space=dict(type='str', required=True),
        environment=dict(type='str', required=True),
        grain_fullname=dict(type='str', required=True),
        resource=dict(type='str', required=True),
        workflow_name=dict(type='str', required=True),
        repository_name=dict(type='str', required=True),
        inputs=dict(type='dict', required=False, default={}),
        owner_email=dict(type='str', required=True),
        execution_name=dict(type='str', required=False),
        api_token=dict(type='str', required=False, no_log=True),
        api_url=dict(type='str', required=False, default='https://portal.qtorque.io')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Get parameters
    space = module.params['space']
    environment = module.params['environment']
    grain_fullname = module.params['grain_fullname']
    resource = module.params['resource']
    workflow_name = module.params['workflow_name']
    repository_name = module.params['repository_name']
    inputs = module.params['inputs']
    owner_email = module.params['owner_email']
    execution_name = module.params['execution_name']
    api_token = module.params['api_token']
    api_url = module.params['api_url']

    # Get API token from environment variable if not provided
    if not api_token:
        api_token = os.environ.get('TORQUE_API_TOKEN')
        if not api_token:
            module.fail_json(msg="API token must be provided either via 'api_token' parameter or 'TORQUE_API_TOKEN' environment variable")

    # Check mode - don't actually execute the workflow
    if module.check_mode:
        module.exit_json(
            changed=True,
            response={"status": "check_mode", "message": "Would execute workflow in normal mode"},
            outputs={}
        )

    # Execute the workflow
    success, response_data, outputs, error_msg = execute_resource_workflow(
        module, space, environment, grain_fullname, resource, workflow_name,
        repository_name, inputs, owner_email, execution_name, api_token, api_url
    )

    if success:
        result = {
            'changed': True,
            'response': response_data,
            'msg': f"Successfully executed workflow '{workflow_name}' on resource '{resource}'"
        }
        
        # Add outputs if present
        if outputs:
            result['outputs'] = outputs
            
        module.exit_json(**result)
    else:
        module.fail_json(
            msg=f"Failed to execute workflow '{workflow_name}' on resource '{resource}': {error_msg}",
            error=error_msg
        )


if __name__ == '__main__':
    main()
