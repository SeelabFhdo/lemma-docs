#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
INCLUSION_FILE="$SCRIPT_DIR/zip_files.txt"
FILES_DIR="$SCRIPT_DIR/.."

# Determine ZIP name from the 'lemma_tour_models_project_name' property in the
# mkdocs.yml configuration file
ZIP_NAME="$(grep "lemma_tour_models_project_name" ../../../../mkdocs.yml | sed -n -e 's/^.*: //p')"
if [ -z "$ZIP_NAME" ]
then
    ZIP_NAME="lemma_tour_models"
fi

TARGET_ZIP_FILE="$FILES_DIR/$ZIP_NAME.zip"
rm -f $TARGET_ZIP_FILE

# Need to change directory so that the zip command will use the correct root
# directory in the created archive
cd "$FILES_DIR"

while read line || [ -n "$line" ];
    do
        if [[ -n "${line/[ ]*\n/}" ]] && ! [[ "$line" =~ ^[\s]*\#.* ]];
        then
            zip -r $TARGET_ZIP_FILE "$line"
        fi
    done < "$INCLUSION_FILE"

# Switch back to directory, from which the script got invoked
cd "$CURRENT_DIR"