#!/bin/bash

TAG="sjghbot-test"

docker run -it \
    --volume `pwd`:/sjghbot \
    --env-file .private/test.list \
    --rm \
    $TAG
