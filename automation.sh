#!/bin/bash
#Use this for docker build
VERSION=v18
APP_NAME=weather-api
#Use this for helm
RELEASE_NAME=weather
NAME_SPACE=default

DOCKER_BUILD=1

if [ "$DOCKER_BUILD" -eq 1 ];then
  docker build -t docker.io/sidharthpai/${APP_NAME}:${VERSION} --no-cache .
  docker push docker.io/sidharthpai/${APP_NAME}:${VERSION}
fi
echo "DOCKER_BUILD is set to false so installing helm"
helm upgrade --install ${RELEASE_NAME} ./python-api -n ${NAME_SPACE} -f ./python-api/values.yaml -f ./python-api/custom-values.yaml
