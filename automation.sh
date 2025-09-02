#!/bin/bash
#Use this for docker build
VERSION=v0.0.1
APP_NAME=weather-api
#Use this for helm
RELEASE_NAME=weather
NAME_SPACE=default

DOCKER_BUILD=1

if [ "$DOCKER_BUILD" -eq 1 ];then
  echo "DOCKER_BUILD is set to true so Bulding the image"
  docker build -t docker.io/sidharthpai/${APP_NAME}:${VERSION} --no-cache .
  echo "DOCKER_BUILD is set to true so Pushing the image"
  docker push docker.io/sidharthpai/${APP_NAME}:${VERSION}
fi
echo "DOCKER_BUILD is set to false so installing helm"
helm upgrade --install ${RELEASE_NAME} ./python-api -n ${NAME_SPACE} -f ./python-api/values.yaml -f ./python-api/custom-values.yaml
