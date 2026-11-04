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

### common.py
Shared helper module used by every script in this project - the Python
equivalent of an Ansible role. Centralizes inventory loading
(`load_inventory`), building a Netmiko connection dict with credentials
pulled from `.env` (`get_device`), and resolving which device(s) to target
based on command-line arguments or falling back to the whole inventory
(`resolve_device_name`). Without this, every script would duplicate the
same boilerplate - exactly the problem Ansible roles solve for playbooks.

### 02_interface_status.py
Connects to one or more devices, runs `show ip int brief` with TextFSM
parsing (via `ntc-templates`, through Netmiko's `use_textfsm=True`), and
flags any interface that isn't both status=up and proto=up. Python
equivalent of `ansible-network-automation/playbooks/02_interface_status.yml`.

TextFSM returns a ready-made list of dictionaries (one per interface)
instead of raw text - no manual `.split()`/line-parsing needed, closing
most of the gap with Ansible's pre-parsed `ios_facts` output. 

### 03_cdp_neighbors.py
Connects to one or more devices, runs `show cdp neighbors detail` with
TextFSM parsing, and prints each neighbor's parsed details. Python
equivalent of `ansible-network-automation/playbooks/03_cdp_neighborss.yml`.

Includes a defensive check (`isinstance(neighbors, list)`) for when TextFSM
fails to match the output against its template - Netmiko doesn't raise an
error in that case, it silently falls back to returning the raw string
instead of a parsed list. Without this check, looping over that string with
`for neighbor in neighbors:` would iterate character-by-character (since
Python loops over a string one character at a time) rather than failing
loudly - a genuinely sneaky bug class worth guarding against any time
`use_textfsm=True` output is consumed downstream.