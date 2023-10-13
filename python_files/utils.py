import json
import os


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "auth.json")
    with open(config_path) as f:
        return json.load(f)
