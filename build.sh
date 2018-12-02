#!/usr/bin/env bash

set -e
py.test

docker build -t genericmoniker/clerkbot .
docker login --username "$DOCKER_USERNAME" --password "$DOCKER_PASSWORD"
docker push genericmoniker/clerkbot
