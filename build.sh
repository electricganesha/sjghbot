#!/bin/bash

VERSION="0.1.0"
TAG="j1fig/sjghbot:$VERSION"

echo Building sjghbot v$VERSION ...

docker build -t $TAG .
docker push $TAG

echo Done!
