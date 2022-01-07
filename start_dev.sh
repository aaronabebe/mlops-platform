#!/bin/sh

docker-compose -f /opt/clearml/docker-compose.yml up -d


echo "WEB UI at:"
echo 'http://localhost:8080'
