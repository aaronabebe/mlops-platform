#!/bin/sh

set -xe

docker-compose -f /opt/clearml/docker-compose.yml down -v
