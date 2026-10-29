import sys
from netmiko import ConnectHandler
from common import load_inventory, get_device, resolve_device_name

def check_interfaces(device_name, inventory):
    try:
        device = get_device(device_name, inventory)
    except ValueError as e:
        print(f"Error is {e}")
        return

    with ConnectHandler(**device) as conn:
        output = conn.send_command("show ip int brief", use_textfsm=True)

    print(f"\n -- {device_name}-- ")
    print(output)

    down_interfaces = []
    for interface in output:
        if interface['status'].lower() != 'up' or interface['proto'].lower() != 'up':
            down_interfaces.append(interface['interface'])

    if len(down_interfaces) > 0:
        print(f"down interfaces are {down_interfaces}")
    else:
        print(f"all interfaces are up on {device_name}")
    
def main():
    inventory = load_inventory()
    device_names = resolve_device_name(sys.argv, inventory)

    for device_name in device_names:
        if device_name not in inventory:
            print(f"Error: '{device_name}' is not found in inventory/devices.yaml")
            continue
        check_interfaces(device_name, inventory)

if __name__ == "__main__":
    main()