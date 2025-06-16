#!/bin/sh

if [ $# -lt 1 ]; then
    CMD=/bin/bash
else
    CMD=$@
fi

docker run -i --workdir /workspace --mount type=bind,source="$(pwd)",target=/workspace --mount type=bind,source="$(pwd)/../../common/",target=/workspace/common --ulimit nofile=8096:8096 -t ti-simplelink-building $CMD
