#!/bin/bash

set -e
set -u

BASE_DIR="$PWD"
RAW_DATA="$BASE_DIR/data/raw"
TMP_DIR="$RAW_DATA/tmp"

mkdir -p "$TMP_DIR"

wget "https://rolandgoecke.net/wp-content/uploads/2019/11/ssbd-release.zip" -O "$TMP_DIR/ssbd-release.zip"
unzip -q "$TMP_DIR/ssbd-release.zip" -d "$TMP_DIR/"
mv "$TMP_DIR/Annotations" "$RAW_DATA/annot"
mv "$TMP_DIR/url-list.pdf" "$RAW_DATA/url-list.pdf"
rm -rf "$TMP_DIR"

python3 "$BASE_DIR/scripts/download_ssbd.py" \
--ann_folder "$RAW_DATA/annot" \
--out_folder "$RAW_DATA/media/" \
--organize
