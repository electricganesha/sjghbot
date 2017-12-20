#!/bin/bash

TAG="sjghbot-local"

echo Building sjghbot-local...

docker build -t $TAG -f Dockerfile.local . > /dev/null

echo Done!
