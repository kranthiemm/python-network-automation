import os
import re
from netmiko import ConnectHandler
from common import get_device, resolve_device_name, load_inventory

def read_hostnames(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def extract_ntp_server(device_name, inventory):
    try:
        device = get_device(device_name, inventory)
    except ValueError as e:
        return f"{device_name}: ERROR - {e}"

    try:
        with ConnectHandler(**device) as conn:
            output = conn.send_command("show run | include ntp server")
    except Exception as e:
        return f"{device_name}: ERROR - could not connect ({e})"

    if not output.strip():
        return f"{device_name}: no NTP server configured"
    
    ntp_servers = re.findall(r"ntp server (\S+)", output)
    return f"{device_name}: {', '.join(ntp_servers)}"



def main():
    inventory = load_inventory()
    hostnames = read_hostnames("hostnames.txt")

    os.makedirs(os.path.dirname("outputs/ntp_results.txt"), exist_ok=True)

    results = []
    for hostname in hostnames:
        if hostname not in inventory:
            result = f"{hostname}: ERROR - not found in inventory/devices.yaml"
        else:
            result= extract_ntp_server(hostname, inventory)
        results.append(result)
        print(result)

    with open("outputs/ntp_results.txt", "w") as f:
        f.write("\n".join(results) + "\n")

    print(f"\nResults written to 'outputs/ntp_results.txt' ")


if __name__ == "__main__":
    main()