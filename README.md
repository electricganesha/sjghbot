sjghbot
=======

Better descriptions will come.

### Pre-requisites

Have [Docker](https://docs.docker.com/engine/installation/#desktop) installed.
If you're on Linux make sure your user is [added to the `docker` group](https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user).


### Development setup

1. Build your local Docker image with local extra useful dependencies with `./build-local.sh`.
2. Running `./run-local.sh` will drop you into the built container bash with all dependencies installed.

Code is mounted on the running container so if you change a file on your host it'll get changed within the
container as well.


### Running tests

1. Build your local test Docker image with extra testing dependencies with `./build-test.sh`.
2. Running `./run-test.sh` will run the tests (uses `pytest`).
