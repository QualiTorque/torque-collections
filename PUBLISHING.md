# How to Publish the Torque Ansible Collection

This guide walks you through the process of publishing the `torque.collections` Ansible collection to Ansible Galaxy.

## Prerequisites

Before publishing, ensure you have:

1. **Ansible installed** with `ansible-galaxy` command available
2. **GitHub account** with access to the `QualiTorque/torque-collections` repository
3. **Ansible Galaxy account** (create at https://galaxy.ansible.com/ using your GitHub account)

### Verify Prerequisites

```bash
# Check if ansible-galaxy is installed
ansible-galaxy --version

# Verify you're in the collection directory
pwd  # Should be /path/to/torque-collections
```

## Step 1: Prepare the Collection

### 1.1 Update Version
Before publishing, update the version in `galaxy.yml`:

```yaml
version: X.Y.Z  # Use semantic versioning (e.g., 1.1.1, 1.2.0, 2.0.0)
```

### 1.2 Validate Collection Structure
Ensure your collection has the proper structure:

```
torque-collections/
├── galaxy.yml
├── README.md
├── LICENSE
├── meta/
│   └── runtime.yml
└── plugins/
    └── modules/
        ├── execute_action.py
        └── export_torque_outputs.py
```

## Step 2: Build the Collection

Build your collection into a distributable tarball:

```bash
# From the collection root directory
ansible-galaxy collection build
```

This creates a file named `torque-collections-X.Y.Z.tar.gz` in your current directory.

### Verify the Build
```bash
# List the generated tarball
ls -la *.tar.gz

# Expected output: torque-collections-X.Y.Z.tar.gz
```

## Step 3: Test Locally (Recommended)

Before publishing, test the collection locally:

```bash
# Install locally for testing
ansible-galaxy collection install torque-collections-X.Y.Z.tar.gz --force

# Verify installation
ansible-galaxy collection list | grep torque
```

## Step 4: Set Up Ansible Galaxy Authentication

### Option A: Using API Token in Command (Quick)

1. Go to https://galaxy.ansible.com/me/preferences
2. Click on "API Key" tab
3. Copy your API token
4. Use it directly in the publish command (see Step 5)

### Option B: Using Configuration File (Recommended)

1. Get your API token from https://galaxy.ansible.com/me/preferences

2. Create the Ansible configuration directory:
   ```bash
   mkdir -p ~/.ansible
   ```

3. Create `~/.ansible/galaxy.yml`:
   ```yaml
   servers:
     galaxy:
       url: https://galaxy.ansible.com/
       token: YOUR_API_TOKEN_HERE
   ```

   Replace `YOUR_API_TOKEN_HERE` with your actual API token.

4. Set appropriate permissions:
   ```bash
   chmod 600 ~/.ansible/galaxy.yml
   ```

## Step 5: Publish to Ansible Galaxy

### Using Option A (Direct Token):
```bash
ansible-galaxy collection publish torque-collections-X.Y.Z.tar.gz --token YOUR_API_TOKEN
```

### Using Option B (Config File):
```bash
ansible-galaxy collection publish torque-collections-X.Y.Z.tar.gz
```

### Publish with Verbose Output:
```bash
ansible-galaxy collection publish torque-collections-X.Y.Z.tar.gz -vvv
```

## Step 6: Verify Publication

1. **Check Ansible Galaxy**: Visit https://galaxy.ansible.com/torque/collections
2. **Test Installation**: Try installing from Galaxy:
   ```bash
   # Install from Galaxy (in a different environment)
   ansible-galaxy collection install torque.collections
   ```

## Publishing Checklist

Before publishing, ensure:

- [ ] Version number updated in `galaxy.yml`
- [ ] `README.md` is up to date with module documentation
- [ ] All modules have proper documentation strings
- [ ] Collection builds without errors
- [ ] Local testing passes
- [ ] GitHub repository is up to date
- [ ] You have a valid Ansible Galaxy API token

## Troubleshooting

### Common Issues:

1. **"Namespace 'torque' not found"**
   - The namespace must be approved on Ansible Galaxy
   - Contact Ansible Galaxy support or use a different namespace

2. **"Version already exists"**
   - You must increment the version number in `galaxy.yml`
   - Each publish requires a unique version

3. **"Invalid collection format"**
   - Ensure `galaxy.yml` has all required fields
   - Check that module files are properly formatted

4. **Authentication Issues**
   - Verify your API token is correct and not expired
   - Check the `~/.ansible/galaxy.yml` file permissions

### Getting Help:

- **Ansible Galaxy Documentation**: https://docs.ansible.com/ansible/latest/galaxy/user_guide.html
- **Collection Development Guide**: https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html
- **Ansible Galaxy Support**: https://github.com/ansible/galaxy/issues

## Future Updates

For subsequent releases:

1. **Update version** in `galaxy.yml`
2. **Update documentation** if needed
3. **Build**: `ansible-galaxy collection build`
4. **Publish**: `ansible-galaxy collection publish torque-collections-X.Y.Z.tar.gz`
5. **Tag release** in GitHub (optional but recommended):
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

## Security Notes

- **Never commit API tokens** to version control
- **Use environment variables** or secure config files for tokens
- **Set proper file permissions** on `~/.ansible/galaxy.yml` (600)
- **Regularly rotate** your API tokens

---

## Quick Reference Commands

```bash
# Build collection
ansible-galaxy collection build

# Install locally for testing
ansible-galaxy collection install torque-collections-X.Y.Z.tar.gz --force

# Publish to Galaxy
ansible-galaxy collection publish torque-collections-X.Y.Z.tar.gz

# Install from Galaxy
ansible-galaxy collection install torque.collections

# List installed collections
ansible-galaxy collection list
```

---

*Last updated: August 2025*
*Collection version: 1.1.0*
