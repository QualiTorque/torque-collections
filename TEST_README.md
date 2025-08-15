# Testing execute_resource_workflow Module

This directory contains test playbooks for the `execute_resource_workflow` Ansible module.

## Files

- `test_execute_resource_workflow.yml` - Main test playbook
- `test_config_template.yml` - Configuration template for test parameters

## Prerequisites

1. **Ansible installed** with the torque.collections collection
2. **Valid Torque API token** set as environment variable `TORQUE_API_TOKEN`
3. **Access to a Torque environment** with valid space, environment, and resources

## Setup

1. **Set your API token:**
   ```bash
   export TORQUE_API_TOKEN="your_api_token_here"
   ```

2. **Configure test parameters:**
   ```bash
   cp test_config_template.yml test_config.yml
   # Edit test_config.yml with your environment details
   ```

3. **Update test variables** in `test_execute_resource_workflow.yml`:
   - `test_space`: Your Torque space name
   - `test_environment`: Target environment ID
   - `test_grain_fullname`: Grain path in the environment
   - `test_resource`: Resource identifier
   - `test_workflow_name`: Workflow/blueprint name to execute
   - `test_repository_name`: Repository containing the workflow
   - `test_owner_email`: Email for workflow execution

## Running Tests

### Run All Tests
```bash
ansible-playbook test_execute_resource_workflow.yml
```

### Run Specific Test Groups
```bash
# Test with minimal parameters only
ansible-playbook test_execute_resource_workflow.yml --tags minimal

# Test with inputs
ansible-playbook test_execute_resource_workflow.yml --tags inputs

# Test custom execution names
ansible-playbook test_execute_resource_workflow.yml --tags custom_name

# Test check mode
ansible-playbook test_execute_resource_workflow.yml --tags check_mode

# Test error handling
ansible-playbook test_execute_resource_workflow.yml --tags error_handling

# Show test summary
ansible-playbook test_execute_resource_workflow.yml --tags summary
```

### Run Individual Tests
```bash
# Run only Test 1
ansible-playbook test_execute_resource_workflow.yml --tags test1

# Run only Test 2
ansible-playbook test_execute_resource_workflow.yml --tags test2

# etc...
```

## Test Descriptions

### Test 1 - Minimal Parameters
Tests the module with only required parameters to verify basic functionality.

### Test 2 - With Inputs
Tests the module with workflow inputs to verify parameter passing.

### Test 3 - Custom Execution Name
Tests the module with a custom execution name to verify naming functionality.

### Test 4 - Custom API URL
Tests the module with a custom API URL parameter.

### Test 5 - Check Mode
Tests the module in check mode to verify it doesn't make actual API calls.

### Test 6 - Error Handling
Tests the module with invalid parameters to verify error handling.

## Expected Output

Successful tests will show:
- `changed: true`
- Response data from the Torque API
- Workflow outputs (if available)

Failed tests (Test 6) will show:
- `failed: true`
- Error messages explaining the failure

## Troubleshooting

### Common Issues

1. **"API token must be provided"**
   - Ensure `TORQUE_API_TOKEN` environment variable is set
   - Or provide `api_token` parameter in the playbook

2. **"API call failed with status 401"**
   - Check that your API token is valid and not expired
   - Verify you have access to the specified space

3. **"API call failed with status 404"**
   - Verify the space name exists
   - Check that the environment ID is correct
   - Ensure the grain and resource exist in the environment

4. **"API call failed with status 400"**
   - Check that the workflow name exists in the repository
   - Verify the repository name is correct
   - Ensure all required workflow inputs are provided

### Debug Mode

Run with increased verbosity to see detailed API calls:
```bash
ansible-playbook test_execute_resource_workflow.yml -vvv
```

## Customizing Tests

To add your own tests:

1. **Add new test tasks** to the playbook
2. **Use appropriate tags** for organization
3. **Register results** to variables for verification
4. **Add assertions** to verify expected behavior

Example:
```yaml
- name: My Custom Test
  torque.collections.execute_resource_workflow:
    space: "{{ test_space }}"
    environment: "{{ test_environment }}"
    grain_fullname: "{{ test_grain_fullname }}"
    resource: "{{ test_resource }}"
    workflow_name: "my-workflow"
    repository_name: "{{ test_repository_name }}"
    owner_email: "{{ test_owner_email }}"
    inputs:
      custom_param: "custom_value"
  register: my_test_result
  tags: [my_test]
```

## Security Notes

- **Never commit** API tokens to version control
- **Use environment variables** or encrypted vault files for sensitive data
- **Limit test scope** to development/test environments when possible
