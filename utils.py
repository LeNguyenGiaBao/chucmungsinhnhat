import json
import os


def read_event_config(event_name):
    config_file_path = os.path.join("./template", event_name, "config.json")
    config = json.load(open(config_file_path))
    config["image_path"] = os.path.join("./template", event_name, config["image_name"])

    return config