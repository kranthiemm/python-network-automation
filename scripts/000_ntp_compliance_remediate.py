import sys
import re
from netmiko import ConnectHandler
from common import load_inventory, get_device, resolve_device_name, load_golden_config


def get_current_ntp_servers(device):
    with ConnectHandler(**device) as conn:
        output = conn.send_command("show run | i ntp server")

    current_servers = re.findall(r"^ntp server (\S+)", output, re.MULTILINE)
    return current_servers


def find_missing_servers(current_servers, golden_servers):
    """Same idea as Ansible's 'difference' filter: golden items not
    already present in current."""
    missing = [s for s in golden_servers if s not in current_servers]
    return missing


def push_missing_servers(device, missing_servers):
    commands = [f"ntp server {s}" for s in missing_servers]
    with ConnectHandler(**device) as conn:
        result = conn.send_config_set(commands)
    return result


def main():
    inventory = load_inventory()
    device_names = resolve_device_name(sys.argv, inventory)
    golden_servers = load_golden_config("ntp")["ntp_servers"]

    for device_name in device_names:
        device = get_device(device_name, inventory)
        current_servers = get_current_ntp_servers(device)

        print(f"\n--- {device_name} ---")
        print(f"Current: {current_servers}")
        print(f"Golden:  {golden_servers}")

        missing = find_missing_servers(current_servers, golden_servers)

        if not missing:
            print("Status: COMPLIANT - nothing to push.")
            continue

        print(f"Status: NOT COMPLIANT - missing: {missing}")
        print("Pushing missing servers...")
        push_result = push_missing_servers(device, missing)
        print(push_result)


if __name__ == "__main__":
    main()