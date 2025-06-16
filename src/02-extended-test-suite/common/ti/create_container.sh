#!/bin/sh
DIR="$(dirname "$(readlink -f "$0")")"

docker build -t ti-simplelink-building - < $DIR/Dockerfile