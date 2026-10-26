# Python Network Automation

Daily Python-based network automation practice, one use case per day, each
committed and pushed on completion. Companion project to
`ansible-network-automation` - same device (R1), same daily discipline,
different tooling (raw Python + Netmiko instead of Ansible), aimed at
interview-level fluency in both.

## Structure
- `scripts/` — daily use-case scripts
- `inventory/devices.yaml` — device inventory (gitignored - real IP/credentials never committed)
- `inventory/devices.yaml.example` — committed template showing the expected structure
- `.env` — secrets, one `<DEVICE_NAME>_PASSWORD=` per device (gitignored)
- `.env.example` — committed template

## Scripts

### 01_gather_facts.py
Connects to one or more devices (via command-line arguments, or every
device in `inventory/devices.yaml` if none are given), using Netmiko, runs
`show version`, and regex-parses hostname/IOS version/serial. Credentials
load from `.env` via `python-dotenv` - the Python equivalent of Ansible's
`.vault_pass` + `vault_password_file`, though notably weaker: Ansible's
vault encrypts the secret value itself even when committed; `.env` relies
entirely on never being committed at all, with no encryption as a backup.