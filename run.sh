#!/bin/bash

TAG="j1fig/sjghbot"
VERSION="0.1.0"

docker pull $TAG:$VERSION

docker run -it \
    --volume `pwd`/data:/sjghbot/data \
    --rm \
    -p 127.0.0.1:8080:8080 \
    $TAG:$VERSION
