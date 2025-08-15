# Ansible Collection - torque.collections

This Ansible collection provides modules for interacting with the Torque platform, enabling you to manage environments, execute actions, and export outputs.

## Installation

Install the collection from Ansible Galaxy:

```bash
ansible-galaxy collection install torque.collections
```

## Modules

### execute_action

Execute actions on resources within a Torque environment.

**Parameters:**
- `space` (required): The Torque space name
- `environment` (required): The environment ID within the space
- `grain_fullname` (required): The grain full name path
- `resource` (required): The resource identifier within the grain
- `action` (required): The action ID to execute
- `api_token` (optional): Torque API token for authentication. If not provided, uses `TORQUE_API_TOKEN` environment variable
- `api_url` (optional): Base URL for the Torque API (default: https://portal.qtorque.io)

**Example Usage:**

```yaml
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
```

### export_torque_outputs

Exports playbook outputs to a JSON file that Torque uses as grain outputs.

**Parameters:**
- `outputs` (required): Dictionary of outputs to export

**Example Usage:**

```yaml
- name: Export outputs
  torque.collections.export_torque_outputs:
    outputs: 
      output1: "{{ result }}"
      database_url: "{{ db_connection_string }}"
      server_ip: "{{ ansible_default_ipv4.address }}"
```

## Authentication

For the `execute_action` module, you can provide authentication in two ways:

1. **Via parameter**: Pass the `api_token` parameter directly
2. **Via environment variable**: Set the `TORQUE_API_TOKEN` environment variable

Example with environment variable:
```bash
export TORQUE_API_TOKEN=your_api_token_here
ansible-playbook your-playbook.yml
```

## Requirements

- Ansible >= 2.9
- Python >= 3.6

## Version History

- **1.1.0**: Added `execute_action` module for executing Torque actions on resources
- **1.0.2**: Initial release with `export_torque_outputs` module

## License

GPL-2.0-or-later

## Authors

- shirel menahem <shirel.m@quali.com>
- DBS
