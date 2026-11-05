import sys
from netmiko import ConnectHandler
from common import get_device, resolve_device_name, load_inventory

def check_vlans(device_name, inventory):
    try:
        device = get_device(device_name, inventory)
    except ValueError as e:
        print(f"Error is {e}")
        return

    with ConnectHandler(**device) as conn:
        vlan = conn.send_command("show vlan brief", use_textfsm=True)

    print(f"--{device_name}--")

    if not isinstance(vlan, list):
        print(f"count not parse vlan output: {vlan}")
        return
    
    if len(vlan) == 0:
        print("No Vlan found")
        return

    print("Parsed VLANs")
    for vl in vlan:
        print(f" {vl}")

def main():
    inventory = load_inventory()
    device_names = resolve_device_name(sys.argv, inventory)

    for device_name in device_names:
        if device_name not in inventory:
            print(f"Error: {device_name} is found in inventory/devices.yaml")
            continue
        check_vlans(device_name, inventory)

if __name__ == "__main__":
    main()