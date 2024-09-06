#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-lammps-repo>"
  exit 1
fi

LAMMPS_PATH=$1

# Verify the provided path is a valid directory
if [ ! -d "$LAMMPS_PATH" ]; then
  echo "Error: Provided path is not a valid directory."
  exit 1
fi

ML_ORB_DIR="$LAMMPS_PATH/src/ML-ORB"
mkdir -p "$ML_ORB_DIR"

cp -r patch/* "$ML_ORB_DIR"

# Modify CMakeLists.txt to include ML-ORB package
CMAKE_LIST="$LAMMPS_PATH/cmake/CMakeLists.txt"
if grep -q "ML-ORB" "$CMAKE_LIST"; then
  echo "ML-ORB package already exists in CMakeLists.txt."
else
  sed -i '/set(STANDARD_PACKAGES/ a\  ML-ORB' "$CMAKE_LIST"
  echo "ML-ORB package added to CMakeLists.txt."
fi

echo "Patch applied successfully!"
