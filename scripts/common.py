import os
import yaml
from dotenv import load_dotenv

def load_inventory(path="inventory/devices.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def get_device(device_name, inventory):
    load_dotenv()
    device_info = inventory[device_name]
    password = os.environ.get(f"{device_name}_PASSWORD")

    if not password:
        raise ValueError(f"{device_name}_PASSWORD not set in .env")

    return {
        "device_type": device_info["device_type"],
        "host": device_info["host"],
        "username": device_info["username"],
        "password": password
    }

def resolve_device_name(argv, inventory):
    if len(argv)>1:
        return argv[1:]
    return list(inventory.keys())