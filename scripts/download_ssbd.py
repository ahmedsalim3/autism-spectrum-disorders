# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:38:52 2025

@author: Ahmed Salim
"""

import xml.etree.ElementTree as ET
import os
import glob
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ann_folder",
        default="data/annot",
        type=str,
        help="Path to the folder containing XML annotation files",
    )
    parser.add_argument(
        "--out_folder",
        default="data/media/ssbd_raw",
        type=str,
        help="Path to the folder where downloaded video files will be saved",
    )
    parser.add_argument(
        "--organize",
        action="store_true",
        help="Flag to organize the downloaded files into category subfolders like ArmFlapping, HeadBanging, Spinning.",
    )
    return parser.parse_args()


def organize_files(ssbd_raw, categories):
    """
    Organize downloaded media files into category directories.
    .
    └── ssbd_raw
        ├── ArmFlapping
        ├── HeadBanging
        └── Spinning
    """
    for category in categories:
        class_dir = os.path.join(ssbd_raw, category)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

    for filename in os.listdir(ssbd_raw):
        if filename.endswith(".avi"):
            for category in categories:
                if category in filename:
                    source = os.path.join(ssbd_raw, filename)
                    destination = os.path.join(ssbd_raw, category, filename)
                    os.rename(source, destination)
                    break


if __name__ == "__main__":

    assert os.system("yt-dlp --version") == 0, "yt-dlp is not installed."

    args = parse_args()

    ann_folder = args.ann_folder
    out_folder = args.out_folder

    xml_files = glob.glob(os.path.join(ann_folder, "*.xml"))
    xml_files.sort()

    for fi in xml_files:
        filename = os.path.splitext(os.path.basename(fi))[0]
        tree = ET.parse(fi)
        root = tree.getroot()
        url = root[0].text

        save_path = os.path.join(out_folder, f"{filename}.avi")

        if not os.path.isfile(save_path):
            command = f"yt-dlp -f best {url} -o {save_path}"
            os.system(command)

    if args.organize:
        categories = ["ArmFlapping", "HeadBanging", "Spinning"]
        organize_files(out_folder, categories)
