import os
import re
import sys
import yaml
from dotenv import load_dotenv
from netmiko import ConnectHandler


def load_inventory():
    with open("inventory/devices.yaml") as f:
        return yaml.safe_load(f)


def gather_facts(device_name, device_info, password):
    device = {
        "device_type": device_info["device_type"],
        "host": device_info["host"],
        "username": device_info["username"],
        "password": password,
    }

    with ConnectHandler(**device) as conn:
        output = conn.send_command("show version")

    hostname_match = re.search(r"^(\S+) uptime", output, re.MULTILINE)
    version_match = re.search(r"Version (\S+),", output)
    serial_match = re.search(r"Processor board ID (\S+)", output)

    print(f"\n--- {device_name} ---")
    print(f"Hostname: {hostname_match.group(1) if hostname_match else 'n/a'}")
    print(f"IOS Version: {version_match.group(1) if version_match else 'n/a'}")
    print(f"Serial: {serial_match.group(1) if serial_match else 'n/a'}")


def main():
    load_dotenv()
    inventory = load_inventory()

    # If a device name was given on the command line, use just that one.
    # Otherwise, loop over every device in the inventory.
    if len(sys.argv) > 1:
        device_names = sys.argv[1:]
        print(device_names)
    else:
        device_names = list(inventory.keys())

    for device_name in device_names:
        if device_name not in inventory:
            print(f"Error: '{device_name}' not found in inventory/devices.yaml")
            continue

        device_info = inventory[device_name]
        password = os.environ.get(f"{device_name}_PASSWORD")

        if not password:
            print(f"Error: {device_name}_PASSWORD not set in .env - skipping {device_name}")
            continue

        gather_facts(device_name, device_info, password)


if __name__ == "__main__":
    main()