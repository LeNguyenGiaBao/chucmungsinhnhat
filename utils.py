import json
import os

import cv2
import numpy as np


def read_event_config(event_name):
    config_file_path = os.path.join("./template", event_name, "config.json")
    config = json.load(open(config_file_path))
    config["image_path"] = os.path.join("./template", event_name, config["image_name"])
    if "is_mask" in config and config["is_mask"]:
        config["mask_path"] = create_mask(config=config)

    return config

def create_mask(config, threshold = 250):
    img_path = config["image_path"]
    mask_path = config["image_path"].replace(config["image_name"], "mask.jpg")
    x, y, width, height = config["x"], config["y"], config['width'], config['height']

    img = cv2.imread(img_path)
    img_w, img_h = img.shape[1], img.shape[0]
    mask_img = np.zeros((img_w, img_h), np.uint8)
    roi_img = img[y:y+height, x:x+width]

    grayscale_image = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(grayscale_image, threshold, 255, cv2.THRESH_BINARY)
    mask_img[y:y+height, x:x+width] = binary_mask
    cv2.imwrite(mask_path, mask_img)

    return mask_path

if __name__ == "__main__":
    config = read_event_config('template_2')
    print(config['mask_path'])
