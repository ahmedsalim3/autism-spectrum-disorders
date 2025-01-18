#!/bin/bash

set -e
set -u

create_dir() {
    local dir="$1"
    [[ ! -d "$dir" ]] && mkdir -p "$dir"
}

BASE_DIR="$PWD"
RAW_DATA="$BASE_DIR/data/raw"
PROCESSED_DATA="$BASE_DIR/data/processed"
TOOLS_BUILD="$BASE_DIR/tools-build"
TOOLS_DIR="$BASE_DIR/tools"
SCRIPT_PATH="$BASE_DIR/scripts/clip_ssbd_videos.py"

create_dir "$PROCESSED_DATA"
create_dir "$TOOLS_BUILD"

cd "$TOOLS_BUILD"
cmake "$TOOLS_DIR"
make

cd "$BASE_DIR"

[[ ! -f "$SCRIPT_PATH" ]] && exit 1

python3 "$SCRIPT_PATH" --ann_folder="$RAW_DATA/annot" \
--origin_folder="$RAW_DATA/media/" --out_folder="$PROCESSED_DATA" \
--height=240 --width=320 --max_num=150
