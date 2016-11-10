#! /bin/sh

ROOT=$(dirname "$(readlink -f "$0")")/../..
INPUT_DIR=$ROOT/pxconvert_input
OUTPUT_DIR=$ROOT/pxconvert_output
IMAGE=20161012-094811-000000001.jpg

# download data
mkdir -p $INPUT_DIR
wget -P $INPUT_DIR \
  http://panorama.urbanexplorer.com.my/MBSA_Crop_Area_Sample/panoramas/$IMAGE


# convert
$ROOT/tools/pxconvert --input $INPUT_DIR --output $OUTPUT_DIR


# prepare the database
createdb panoramix
psql panoramix -c "create extension postgis;"

# convert
mkdir -p $ROOT/pxvips_output
$ROOT/tools/px2pg $ROOT/tests/tools/pxserver.yml equi $OUTPUT_DIR
