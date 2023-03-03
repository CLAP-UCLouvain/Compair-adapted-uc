#!/bin/bash
COMPAIR_PATH="$HOME/compair-adapted-uc"
if [ "$PWD" != "$COMPAIR_PATH" ];
then
 pushd "$COMPAIR_PATH"
 sudo docker-compose stop && sudo docker-compose rm -f
 sudo docker build -t uclouvain/uclouvain-compair:latest . > /dev/null && sudo docker-compose up -d
 popd
else
 sudo docker-compose stop && sudo docker-compose rm -f
 sudo docker build -t uclouvain/uclouvain-compair:latest . > /dev/null && sudo docker-compose up -d
fi
