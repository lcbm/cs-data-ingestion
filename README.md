# 📝 Data Ingestion Proof of Concept

This repository contains the specification for the _**third deliverable of the 'Projects' class**_. Currently, the services are organized as a [Docker swarm](https://docs.docker.com/engine/swarm/key-concepts/) stack in `compose.yml`.

## Contents

- [Development](#development)
- [Deploying the Stack](#deploying-the-stack)
- [Contributing](#contributing)
- [LICENSE](#license)

## Development

To install the **development pre-requisites**, please follow the instructions in the links below:

- [Python 3.8](https://www.python.org/downloads/)
- [Poetry](https://github.com/python-poetry/poetry#installation)

### Installing development dependencies

First, change your current working directory to the project's root directory and bootstrap the project:

```bash
# change current working directory
$ cd <path/to/cs-data-ingestion>

# bootstraps development and project dependencies
$ make bootstrap
```

>_**NOTE**: By default, [poetry creates and manages virtual environments to install project dependencies](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment) -- meaning that it will work isolated from your global Python installation. This avoids conflicts with other packages installed in your system._

## Deploying the Stack

### Requirements

Considering that the stack is organized as a [Docker swarm](https://docs.docker.com/engine/swarm/key-concepts/) stack, the following dependencies must be installed:

- [Docker](https://docs.docker.com/get-docker/)

>**_NOTE_**: If you're using a Linux system, please take a look at [Docker's post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)!

### Setup

Once you have `Docker` installed, pull the Docker images of the services used by the stack:

```bash
# fetches services' docker images
$ make docker-pull
```

Finally, update the `env.d` files for each service with the appropriate configurations, credentials, and any other necessary information.

>**_NOTE_**: in order to generate a [fernet key](https://airflow.readthedocs.io/en/stable/howto/secure-connections.html) for Airflow, please take a look [here](https://beau.click/airflow/fernet-key).

### Initialize Swarm mode

In your deployment machine, initialize Docker Swarm mode:

```bash
# joins the swarm
$ docker swarm init
```

> **_Note:_**  For more information on what is Swarm and its key concepts, please refer to [Docker's documentation](https://docs.docker.com/engine/swarm/key-concepts/).

### Deploying services

Now that the deployment machine is in swarm mode, deploy the stack:

```bash
# deploys/updates the stack from the specified file
$ docker stack deploy -c compose.yml cs-data-ingestion
```

### Verifying the Stack's Status

Check if all the services are running and have **exactly one** replica:

```bash
# list the services in the cs-data-ingestion stack
$ docker stack services cs-data-ingestion
```

You should see something like this:

```text
ID                  NAME                            MODE                REPLICAS            IMAGE                               PORTS
9n8ldih68jnk        cs-data-ingestion_redis               replicated          1/1                 bitnami/redis:6.0
f49nmgkv3v9i        cs-data-ingestion_airflow             replicated          1/1                 bitnami/airflow:1.10.13             *:8080->8080/tcp
fxe80mcl98si        cs-data-ingestion_postgresql          replicated          1/1                 bitnami/postgresql:13.1.0
ii6ak931z3so        cs-data-ingestion_airflow-scheduler   replicated          1/1                 bitnami/airflow-scheduler:1.10.13
vaa3lkoq133d        cs-data-ingestion_airflow-worker      replicated          1/1                 bitnami/airflow-worker:1.10.13
```

At this point, the following resources will be available to you:

- [Airflow Webserver](https://airflow.apache.org) UI is available at `http://localhost:8080`

>**_NOTE:_**  In case `localhost` doesn't work, you may try `http://0.0.0.0:<port>` instead.

### Logging

In order to check a service's logs, use the following command:

```bash
# fetch the logs of a service
$ docker service logs <service_name>
```

>**_NOTE:_**  You may also follow the log output in realtime with the `--follow` option (e.g. `docker service logs --follow cs-data-ingestion_airflow`). For more information on service logs, refer to [Docker's documentation](https://docs.docker.com/engine/reference/commandline/service_logs/).

### Wrapping up

Once you're done, you may remove what was created by `docker swarm init`:

```bash
# removes the cs-data-ingestion stack from swarm
$ docker stack rm cs-data-ingestion

# leaves the swarm
$ docker swarm leave
```

>**_NOTE:_**  All the data created by the stack services will be lost. For more information on swarm commands, refer to [Docker's documentation](https://docs.docker.com/engine/reference/commandline/swarm/).

## Contributing

We are always looking for contributors of **all skill levels**! If you're looking to ease your way into the project, try out a [good first issue](https://github.com/lcbm/cs-data-ingestion/labels/good%20first%20issue).

If you are interested in helping contribute to the project, please take a look at our [Contributing Guide](CONTRIBUTING.md). Also, feel free to drop in our [community chat](https://gitter.im/lcbm/community) and say hi. 👋

Also, thank you to all the [people who already contributed](https://github.com/lcbm/cs-data-ingestion/graphs/contributors) to the project!

## License

Copyright © 2020-present, [CS Data Ingestion Contributors](https://github.com/lcbm/cs-data-ingestion/graphs/contributors).
This project is [ISC](LICENSE) licensed.
