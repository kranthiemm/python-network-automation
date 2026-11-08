import sys
from netmiko import ConnectHandler
from common import load_inventory, get_device, resolve_device_name

VLAN_ID = 100
VLAN_NAME = "vlan_test"

def vlan_already_exist(conn, vlan_id):
    output = conn.send_command("show vlan brief", use_textfsm=True)
    if not isinstance(output, list):
        return False
    found = False
    for v in output:
        if str(v.get("vlan_id")) == str(vlan_id):
            found = True
            break
    return found

def push_vlan(device_name, inventory):
    device = get_device(device_name, inventory)

    with ConnectHandler(**device) as conn:
        print(f"--{device_name}--")

        if vlan_already_exist(conn, VLAN_ID):
            print(f"VLAN {VLAN_ID} already exists - nothing to do (idempotent).")
            return

        print(f"VLAN {VLAN_ID} not found - creating it...")
        commands = [
            f"vlan {VLAN_ID}",
            f"name {VLAN_NAME}",
        ]
        result = conn.send_config_set(commands)
        print(result)

def main():
    inventory = load_inventory()
    device_names = resolve_device_name(argv, inventory)

    for device_name in device_names:
        if device_name not in inventory:
            print(f"Error: '{device_name}' not found in inventory/devices.yaml")
            continue
        push_vlan(device_name, inventory)

if __name__ == "__main__":
    main() 