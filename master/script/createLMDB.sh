#!/bin/bash

# createLMDB: Quick and easy way to turn videos and images into a LMDB caffe-ready database and mean binaryproto file!
# Developed @ TCNJ

# Enviornment Variables =======================================================

OUTPUT_PATH=$HOME

CAFFE_TOOLS_PATH=/home/caffe/build/tools

IMG_WIDTH=--resize_width=256

IMG_HEIGHT=--resize_height=256

# =============================================================================

# Constants ===================================================================
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TMP_NAME=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 5)

INPUT_CMD="$*"
# =============================================================================


# Shows HELP information for this script
if [ "$#" == 0 ] || [ "$*" == -h ]; then
        echo " "
        echo "---------------------------------------------------------- createLMDB ---------------------------------------------------------------------------"
        echo " "
        echo "Description: Hello! This is createLMDB a script that can take various inputs and create an LMDB database and mean binaryproto file!"
        echo "Inputs: A directory with images (png, jpg, bmp, etc) AND/OR a path to a video file."
        echo "Output: By default, will create a LMDB database and a mean binaryproto in the current user's home directory named a random string"
        echo ""
        echo "Basic Use:"
        echo "./createLMDB.sh <path1> <class1> <path2> <class2> <path3> <class3> ..."
        echo ""
        echo "Basic Example:"
        echo "./createLMDB.sh grassOnly/ 0 weedAndGrass/ 1 videos/videoOfOnlyGrass.mp4 0 videos/videoOfGrassAndWeeds.mov 1"
        echo "              ^^^^^^^^^  ^                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^"
        echo "              Directory  class number                 Video            class number"
        echo ""
        echo ""
        echo "Advanced Use:"
        echo "./createLMDB.sh --shuffle --gray <path1> <class1> <path2> <class2> <path3> <class3> ..."
        echo ""
        echo "Advanced Example:"
        echo "./createLMDB.sh --shuffle --gray grassOnly/ 0 weedAndGrass/ 1 videos/videoOfOnlyGrass.mp4 0 videos/videoOfGrassAndWeeds.mov 1"
        echo "              ^^^^^^^^^ ^^^^^^              ^^^^^^^^^^^^  ^                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^"
        echo "              Optional  Optional            Directory     class number                                 Video              class number"
        echo ""
        echo ""
        echo "(Build 2.1.1)"
        echo "-------------------------------------------------------------------------------------------------------------------------------------------------"
        echo ""
        exit 0
fi


# Checks for the option to make all the images in the database gray
DB_FLAG1=""
if [ "$1" == --gray ] || [ "$1" == --shuffle ]; then
        DB_FLAG1=$1
        shift
fi


# Checks for the option to make all the images shuffle around when creating the database
DB_FLAG2=""
if [ "$1" == --gray ] || [ "$1" == --shuffle ]; then
        DB_FLAG2=$1
        shift
fi


# Processing Directory of Images
function processDirectory
{
        # Create temporary processing directory
        RANDOM_STR=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)
        mkdir /tmp/$TMP_NAME/$RANDOM_STR

        # Copies images from input directory into the processing directory
        for entry in "$1"/*; do
            cp $entry /tmp/$TMP_NAME/$RANDOM_STR
        done

        # Detects the number of images in the input directory. Used for naming
        IMG_COUNT=$(ls -l /tmp/$TMP_NAME/img/$2 | grep -v ^d | wc -l)

        if [ "$IMG_COUNT" != 1 ]; then
                ((IMG_COUNT++))
        fi

        # Moves the images from the processing directory into the build directory
        for entry in "/tmp/$TMP_NAME/$RANDOM_STR"/*; do
            mv -i $entry /tmp/$TMP_NAME/img/$2/$2-`printf %07d $IMG_COUNT`.${entry##*.}
            ((IMG_COUNT++))
        done

        # Remove the process directory (cleanup)
        rm -r /tmp/$TMP_NAME/$RANDOM_STR
}


# Processing Video Files (generates BMPs for each video frame)
function processVideo
{
        # Create Temp processing video directory
        RANDOM_STR=$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)
        mkdir /tmp/$TMP_NAME/$RANDOM_STR

        # Process Video using FFMPEG Library
        $SCRIPT_DIR/library/ffmpeg/ffmpeg -hide_banner -i $1 -r 1/1 /tmp/$TMP_NAME/$RANDOM_STR/%d.bmp

        # Get the # of videos in the build directory
        IMG_COUNT=$(ls -l /tmp/$TMP_NAME/img/$2 | grep -v ^d | wc -l)

        if [ "$IMG_COUNT" != 1 ]; then
                ((IMG_COUNT++))
        fi

        # Rename and moving processed images from videos to the build directory
        for entry in "/tmp/$TMP_NAME/$RANDOM_STR"/*; do
                mv -i $entry /tmp/$TMP_NAME/img/$2/$2-`printf %07d $IMG_COUNT`.${entry##*.}
                ((IMG_COUNT++))
        done

        # Remove the process directory (cleanup)
        rm -r /tmp/$TMP_NAME/$RANDOM_STR
}


echo " "
echo "-------------- createLMDB ---------------"
echo " "

        # Sets up the build directory
        mkdir /tmp/$TMP_NAME /tmp/$TMP_NAME/img

        while [ $# -gt 0 ]; do

                INPUT_DIR=$1
		echo "createLMDB > Preparing $INPUT_DIR"
                shift

                if [ ! -d "/tmp/$TMP_NAME/img/$1" ]; then
                        mkdir /tmp/$TMP_NAME/img/$1
                fi

                if [ -d "$INPUT_DIR" ]; then
                        processDirectory $INPUT_DIR $1

                elif [ -f "$INPUT_DIR" ]; then
                        processVideo $INPUT_DIR $1

                else
                        echo "createLMDB > Input does not exist! (Stopped)"
                        echo " "
                        echo "----------------------------------------"
                        echo " "

                        # Error. Completely scrap the build process
                        rm -r /tmp/$TMP_NAME

                        exit 0
                fi

                shift
        done


# Writes to the label text file with the path to each image and an associated label number

    if [ -f /tmp/$TMP_NAME/labels.txt ]; then
        rm /tmp/$TMP_NAME/labels.txt
    fi

    touch /tmp/$TMP_NAME/labels.txt

    for entry1 in "/tmp/$TMP_NAME/img"/*; do
        for entry2 in "$entry1"/*; do
            echo "$entry2 $(basename $entry1)" >> /tmp/"$TMP_NAME"/labels.txt
         done
    done


# Take the images (in a destination folder) and creates a lmdb database:

    cd $SCRIPT_DIR
    cd ..

    $CAFFE_TOOLS_PATH/convert_imageset $DB_FLAG1 $DB_FLAG2 / /tmp/$TMP_NAME/labels.txt $OUTPUT_PATH/$TMP_NAME

    cd $SCRIPT_DIR


# Saves the label file for analysis
    
    cp /tmp/$TMP_NAME/labels.txt $OUTPUT_PATH/$TMP_NAME/labels.txt


# Logs the command that made the generated database

    touch $OUTPUT_PATH/$TMP_NAME/build_log.txt
    echo "-------------------- Build Log -------------------" >> $OUTPUT_PATH/$TMP_NAME/build_log.txt
    echo "" >> $OUTPUT_PATH/$TMP_NAME/build_log.txt
    echo "$SCRIPT_DIR/createLMDB.sh $INPUT_CMD" >> $OUTPUT_PATH/$TMP_NAME/build_log.txt


# Creates a mean file out of the newly created database

    $CAFFE_TOOLS_PATH/compute_image_mean $OUTPUT_PATH/$TMP_NAME/ $OUTPUT_PATH/$TMP_NAME/mean.binaryproto


# Deletes the temporary location that held processed images

    rm -r /tmp/$TMP_NAME


# Shows the location of generated database/mean file

    echo " "
    echo "createLMDB > Your LMDB database and mean file were created in $OUTPUT_PATH/$TMP_NAME for your caffe consumption!"
    echo "createLMDB > Enjoy! :)"
    echo " "
    echo "----------------------------------------"
