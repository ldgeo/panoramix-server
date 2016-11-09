#! /bin/bash

# -----------------------------------------------------------------------------
# read cli
# -----------------------------------------------------------------------------
while [ $# -gt 1 ]
do
  key="$1"

  case $key in
    --input)
      INPUT_DIR="$2"
      shift
     ;;

    --output)
      OUTPUT_DIR="$2"
      shift
    ;;
  esac

  shift
done

if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]
then
    echo "Invalid usage: "
    echo "  pxvips.sh --input <input_dir> --output <output_dir>"
    exit
fi

# -----------------------------------------------------------------------------
# vips
# -----------------------------------------------------------------------------
FILES=$(find $INPUT_DIR -regex ".*\.\(jpg\|gif\|png\|jpeg\)")

for f in $FILES
do
  echo "Converting $f..."
  FILENAME=$(basename $f)
  FILENAME_BASE=$(echo $FILENAME | cut -f 1 -d '.')
  FILENAME_DIR=$(dirname $f)
  OUTPUT_SUBDIR=${FILENAME_DIR#$(dirname "$(dirname "$f")")/}

  mkdir -p $OUTPUT_DIR/$OUTPUT_SUBDIR
  vips im_vips2tiff $f \
    $OUTPUT_DIR/$OUTPUT_SUBDIR/$FILENAME_BASE.tif:deflate,tile:256x256,pyramid
done
