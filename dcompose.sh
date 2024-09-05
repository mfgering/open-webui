#!/bin/bash

echo "1: $1"

if [ "$1" == "" ]; then
    OP="up"
else
    OP="$1"
fi
echo "1: $1, OP=$OP"

# Use getopt to parse long and short options
ARGS=$(getopt -o "u:" --long "up" -n "$0" -- "$@")
eval set -- "$ARGS";

# Initialize up variable, default is 'up'
UP="up";

while true; do
    case $1 in
        -u|--up) shift; UP=$1;;
        --) shift; break ;;
    esac
done

echo "Using UP value: $UP"
