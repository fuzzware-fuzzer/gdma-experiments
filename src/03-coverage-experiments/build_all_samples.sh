#/bin/bash
# script to iterate through all target directories and call the respective build script
# the rebuilt targets will be in $build_name/output/$sample_name/$sample.elf
set -x 
DIR="$(dirname "$(readlink -f "$0")")"

# build the base image
cd "$DIR/../02-extended-test-suite/common/"
docker build . -t password-base
cd $DIR
# export IMPORT_IMAGES=1 

find $DIR -name build_docker.sh -execdir sh build_docker.sh \;
# for build_script in "$DIR"/*/build_docker.sh;
# do
#     cd "$(dirname "$build_script")"
#     "$build_script"
# done
