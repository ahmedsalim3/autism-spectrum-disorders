# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:38:45 2025

@author: Ahmed Salim
"""

import xml.etree.ElementTree as ET
import os
import glob
import argparse
import sys
import shlex


def parse_args():
    parser = argparse.ArgumentParser(
        description="Clip SSBD dataset based on Categories. This script processes video files and clips segments based on annotation categories such as armflapping, headbanging, and spinning."
    )
    parser.add_argument(
        "--ann_folder",
        dest="ann_folder",
        default="/data/raw/annot",
        type=str,
        help="Path to the folder containing XML annotation files",
    )
    parser.add_argument(
        "--origin_folder",
        dest="origin_folder",
        default="/data/raw/media",
        type=str,
        help="Path to the folder containing the original video files",
    )
    parser.add_argument(
        "--out_folder",
        dest="out_folder",
        default="/data/ssbd_clip_segment",
        type=str,
        help="Path to the output folder where clipped video segments will be saved",
    )
    parser.add_argument(
        "--height",
        dest="height",
        default=240,
        type=int,
        help="Height of the clipped video segments",
    )
    parser.add_argument(
        "--width",
        dest="width",
        default=320,
        type=int,
        help="Width of the clipped video segments",
    )
    parser.add_argument(
        "--max_num",
        dest="max_num",
        default=200,
        type=int,
        help="Maximum number of clips per category",
    )

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    ann_folder = args.ann_folder
    origin_folder = args.origin_folder
    out_folder = args.out_folder
    height = args.height
    width = args.width
    max_num = args.max_num

    if not os.path.isdir(ann_folder):
        print(f"Error: Annotation folder {ann_folder} does not exist.")
        sys.exit(1)

    if not os.path.isdir(origin_folder):
        print(f"Error: Origin folder {origin_folder} does not exist.")
        sys.exit(1)

    if not os.path.isdir(out_folder):
        print(f"Error: Output folder {out_folder} does not exist.")
        sys.exit(1)

    xml_files = glob.glob(os.path.join(ann_folder, "*.xml"))
    xml_files.sort()

    for fi in xml_files:

        filename = os.path.splitext(os.path.basename(fi))[0]
        classname = filename[2:-3]
        tree = ET.parse(fi)
        root = tree.getroot()

        input_video = os.path.join(origin_folder, classname, "%s.avi" % (filename))
        if not os.path.isfile(input_video):
            print(f"Warning: Video file {input_video} not found. Skipping.")
            continue

        print(f"Clipping video {filename}...")

        duration = root.find("duration").text
        behaviours = root.find("behaviours")
        for behaviour in behaviours:
            time = behaviour.find("time").text
            cat = behaviour.find("category").text

            if cat == "armflapping":
                out_class = "ArmFlapping"
            elif cat == "headbanging":
                out_class = "HeadBanging"
            elif cat == "spinning":
                out_class = "Spinning"
            else:
                print(f"Error: Illegal category {cat} found in {fi}. Exiting.")
                sys.exit(1)

            out_class_folder = os.path.join(out_folder, out_class)
            if not os.path.isdir(out_class_folder):
                os.makedirs(out_class_folder)

            cnt = len(glob.glob(os.path.join(out_class_folder, "*.avi")))
            cnt += 1
            save_file = os.path.join(out_class_folder, f"{cnt:02d}.avi")
            if os.path.isfile(save_file):
                continue

            cmd = f"tools-build/clip_segment -i={shlex.quote(input_video)} -t={shlex.quote(time)} -o={shlex.quote(save_file)} -d={shlex.quote(duration)} -h={height} -w={width} -m={max_num}"
            os.system(cmd)
