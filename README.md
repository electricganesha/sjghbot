sjghbot
=======

Better descriptions will come.

### Pre-requisites

Have [Docker](https://docs.docker.com/engine/installation/#desktop) installed.
If you're on Linux make sure your user is [added to the `docker` group]
(https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

`sjghbot` expects you to have properly set environment variable lists to pass to `docker run`.
These live in `.private/<env>.list` files, where `<env>` can be `local`, `test` and `prod`.
Be sure to follow the [official example]
(https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e-env-env-file).
These are currently the vars you're expected to set:

    $ cat .private/local.list 
    SJGHBOT_POLONIEX_KEY=you
    SJGHBOT_POLONIEX_SECRET=wish
    SJGHBOT_TWITTER_CONSUMER_KEY=sad98yua9s8dyuasd
    SJGHBOT_TWITTER_CONSUMER_SECRET=asjdpoa8usd098ua98syud9yads
    SJGHBOT_TWITTER_ACCESS_TOKEN_KEY=oiHJU98yua9s8dyu9aysd9hya9syd9a8ys9d
    SJGHBOT_TWITTER_ACCESS_TOKEN_SECRET=kjnamnxnclkasdahsdhwlkh


### Development setup

1. Build your local Docker image with local extra useful dependencies with `./build-local.sh`.
2. Running `./run-local.sh` will drop you into the built container bash with all dependencies installed.

Code is mounted on the running container so if you change a file on your host it'll get changed within the
container as well.


### Running tests

1. Build your local test Docker image with extra testing dependencies with `./build-test.sh`.
2. Running `./run-test.sh` will run the tests (uses `pytest`).


### Deploying and running

Note: I realize this deployment process can be simplified a bit - still a WIP.

1. If you want to make a new release, up the $VERSION in `./build.sh` and run it.
2. From your server/machine of choice, clone this repo.
3. `run.sh` - this pulls and runs the image you just pushed.

Databases/assets get mounted on the `data/` directory on the root of your repo.
