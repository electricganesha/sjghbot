#!/bin/bash

TAG="sjghbot-test"

echo Building sjghbot-test...

docker build -t $TAG -f Dockerfile.test . > /dev/null

echo Done!
