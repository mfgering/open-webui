#!/bin/bash

login_to_docker() {
  # Capture the output and return code of docker-login.sh
  output=$(docker-login.sh 2>&1)
  return_code=$?

  # Check if the return code indicates failure
  if [ $return_code -ne 0 ]; then
    echo "Error: docker-login.sh failed with return code $return_code"
    echo "Output: $output"
    exit 1
  else
    echo "Logged in"
  fi
}

# Call the login function
login_to_docker
export WEBUI_DOCKER_TAG=main
docker pull ghcr.io/open-webui/open-webui:${WEBUI_DOCKER_TAG}
# Build mgering/open-webui:main from Dockerfile.mfg
docker build --build-arg WEBUI_DOCKER_TAG=${WEBUI_DOCKER_TAG} -t mgering/open-webui:main -f Dockerfile.mfg .
docker push mgering/open-webui:main