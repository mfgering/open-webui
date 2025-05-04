#!/bin/bash
# NOTE: the .env file has API keys, etc

# Default operation
OP="up"

# Process arguments
while (( "$#" )); do
  case "$1" in
    -d)
      DETACH="--detach"
      shift
      ;;
    *)
      # Assume it's the operation if not a known flag
      OP=$1
      shift
      ;;
  esac
done

# Load environment variables
source .env

# Execute Docker Compose command
docker compose -f docker-compose.yaml -f docker-compose.amdgpu.yaml -f docker-compose.api.yaml -f docker-compose.mfg.yaml $OP $DETACH