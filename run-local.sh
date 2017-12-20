#!/bin/bash

TAG="sjghbot-local"

docker run -w /sjghbot \
    -it \
    --volume `pwd`:/sjghbot \
    --env-file .private/local.list \
    --rm \
    -p 127.0.0.1:8080:8080 \
    $TAG \
    /bin/bash
