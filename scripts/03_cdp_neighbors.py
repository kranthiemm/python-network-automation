import sys
from netmiko import ConnectHandler
from common import load_inventory, get_device, resolve_device_name

def check_cdp_neighbors(device_name, inventory):
    try:
        device = get_device(device_name, inventory)
    except ValueError as e:
        print(f"Error: {e}")
        return

    with ConnectHandler(**device) as conn:
        neighbors = conn.send_command("show cdp neighbor detail", use_textfsm=True)

    print(f"\n---{device_name}---")
    
    if not isinstance(neighbors, list):
        print(f"Could not parse CDP output (CDP likely disabled or unsupported): {neighbors.strip()}")
        return


    if len(neighbors) == 0:
        print("No CDP neighbors found - check CDP is enabled, or no neighbors exist.")
        return

    print("\nParsed neighbors:")
    for neighbor in neighbors:
        print(f"{neighbor}")

def main():
    inventory = load_inventory()
    device_names= resolve_device_name(sys.argv, inventory)

    for device_name in device_names:
        if device_name not in inventory:
            print(f"Error: '{device_name}' not found in inventory/devices.yaml")
            continue
        check_cdp_neighbors(device_name, inventory)


if __name__ == "__main__":
    main()
