#!/bin/bash

TAG="j1fig/sjghbot"
VERSION="0.1.0"

docker pull $TAG:$VERSION

docker run -w /sjghbot \
    -it \
    --volume `pwd`/data:/sjghbot/data \
    --env-file .private/local.list \
    --rm \
    -p 127.0.0.1:8080:8080 \
    $TAG:$VERSION \
    /bin/bash
