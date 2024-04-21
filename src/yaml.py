import yaml
from src.connection import Connection
# Important variables
with open("config.yml", "r") as f:
    load = yaml.safe_load(f)
    token = load["token"]
    status = load["status"]
    owner_id = load["owner_id"]
    switchip = load["switchip"]
    guild = load["debug_guilds"]
    url = load["url"]
    delay = load["delay"]

# Prevent circular import.
connect = Connection(switchip)
