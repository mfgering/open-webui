#!/bin/bash
#NOTE: the .env file has API keys, etc
if [ "$1" == "" ]; then
    OP="up"
else
    OP="$1"
fi

source .env && docker compose -f docker-compose.yaml -f docker-compose.amdgpu.yaml -f docker-compose.api.yaml -f docker-compose.mfg.yaml $OP
