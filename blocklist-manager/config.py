# config.py
import json
import os

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config(config_file=DEFAULT_CONFIG_FILE):
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

# Example structure of config.json:
# {
#     "urls": [
#         "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt",
#         "https://adguardteam.github.io/HostlistsRegistry/assets/filter_49.txt",
#         ...
#     ],
#     "download_dir": ".",
#     "default_output": "merged_blocklist.txt",
#     "default_whitelist": "whitelist.txt",
#     "default_max_age": 24
# }