#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: execute_action

short_description: Execute a Torque action on a resource within an environment

version_added: "1.1.0"

description: 
    - This module allows executing actions on resources within a Torque environment
    - Calls the Torque API endpoint to trigger actions on specific resources

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
    action:
        description:
            - The action ID to execute
        required: true
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
- name: Execute action on AWS instance
  torque.collections.execute_action:
    space: 03-Live
    environment: tuF7LfdwbCs4
    grain_fullname: elk-2
    resource: aws_instance.elk_2
    action: aws-power-on-ec2-tf
    api_token: "{{ torque_api_token }}"

- name: Execute action using environment variable for token
  torque.collections.execute_action:
    space: production
    environment: env_12345
    grain_fullname: web-server
    resource: aws_instance.web_1
    action: restart-service
'''

RETURN = r'''
response:
    description: API response from the action execution
    returned: always
    type: dict
    sample: {
        "status": "success",
        "message": "Action executed successfully",
        "execution_id": "exec_12345"
    }
'''

import os
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def execute_torque_action(module, space, environment, grain_fullname, resource, action, api_token, api_url):
    """Execute a Torque action via API call"""
    
    # Construct the API endpoint
    endpoint = f"/api/spaces/{space}/environments/{environment}/{grain_fullname}/{resource}/run_action/{action}"
    url = f"{api_url.rstrip('/')}{endpoint}"
    
    # Prepare headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Prepare request body
    body = json.dumps({"force": False})

    # Make the API call
    try:
        response, info = fetch_url(
            module=module,
            url=url,
            method='POST',
            headers=headers,
            data=body,
            timeout=30
        )
        
        # Check response status
        if info['status'] == 200 or info['status'] == 201:
            try:
                response_data = json.loads(response.read().decode('utf-8'))
                return True, response_data, None
            except (ValueError, TypeError):
                return True, {"status": "success", "message": "Action executed successfully"}, None
        else:
            error_msg = f"API call failed with status {info['status']} and message: {info.get('msg', '')}"
            try:
                error_body = response.read().decode('utf-8') if response else info.get('body', '')
                if error_body:
                    error_data = json.loads(error_body)
                    error_msg = error_data.get('message', error_msg)
            except:
                pass
            return False, None, error_msg
            
    except Exception as e:
        return False, None, f"Error making API call: {str(e)}"


def main():
    module_args = dict(
        space=dict(type='str', required=True),
        environment=dict(type='str', required=True),
        grain_fullname=dict(type='str', required=True),
        resource=dict(type='str', required=True),
        action=dict(type='str', required=True),
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
    action = module.params['action']
    api_token = module.params['api_token']
    api_url = module.params['api_url']

    # Get API token from environment variable if not provided
    if not api_token:
        api_token = os.environ.get('TORQUE_API_TOKEN')
        if not api_token:
            module.fail_json(msg="API token must be provided either via 'api_token' parameter or 'TORQUE_API_TOKEN' environment variable")

    # Check mode - don't actually execute the action
    if module.check_mode:
        module.exit_json(
            changed=True,
            response={"status": "check_mode", "message": "Would execute action in normal mode"}
        )

    # Execute the action
    success, response_data, error_msg = execute_torque_action(
        module, space, environment, grain_fullname, resource, action, api_token, api_url
    )

    if success:
        module.exit_json(
            changed=True,
            response=response_data,
            msg=f"Successfully executed action '{action}' on resource '{resource}'"
        )
    else:
        module.fail_json(
            msg=f"Failed to execute action '{action}' on resource '{resource}': {error_msg}",
            error=error_msg
        )


if __name__ == '__main__':
    main()
