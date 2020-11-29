# 📝 Data Ingestion Proof of Concept

This repository contains the specification for the _**third deliverable of the 'Projects' class**_. Currently, the services are organized as [Docker swarm](https://docs.docker.com/engine/swarm/key-concepts/) stack in `compose.yml` and the infrastructure is organized in [Terraform](https://www.terraform.io) files in `terraform/`.

## Contents

- [Development](#development)
- [Deploying the Stack](#deploying-the-stack)
  - [Terraform](#terraform)
  - [Docker](#docker)
- [Contributing](#contributing)
- [LICENSE](#license)

## Development

To install the **development pre-requisites**, please follow the instructions in the links below:

- [Python 3.8](https://www.python.org/downloads/)
- [Poetry](https://github.com/python-poetry/poetry#installation)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

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

If you wish to deploy the stack locally, jump to the [Docker](#docker) section. If you wish to deploy the services to AWS, on the other hand, continue to the [Terraform](#terraform) section.

### Terraform

Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers by generating an execution plan describing what it will do to reach the desired state (described in the project's Terraform files), and then executes it to build the described infrastructure. As the configuration changes, Terraform is able to determine what changed and create incremental execution plans which can be applied. For this project, the infrastructure is deployed to [AWS](aws.amazon.com).

#### Configuring AWS Credentials

Follow the instructions in AWS CLI [documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) to configure your AWS account locally. After that, update the variable `profile` to point to your account profile.

#### Deploying Infrastructure

After you're done configuring your AWS profiles, change your current working directory to where `Terraform` files are located and initialize it:

```bash
# change current working directory
$ cd terraform

# prepares the current working directory for use
$ terraform init
```

Now, apply the changes required to reach the desired state of the configuration described in the Terraform files. Make sure to correctly reference your [SSH Key Pair](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-2) or else Terraform won't be able to deploy the project's services:

```bash
# applies required changes and passes the SSH key pair as parameters
$ terraform apply -var 'key_name=key' -var 'public_key_path=~/.ssh/key.pub'
```

>**_Note:_** Make sure the output for `SSH Agent` is `true`: `SSH Agent: true`. In case it isn't, please run `$ eval "$(ssh-agent -s)"` and `$ ssh-add ~/.ssh/key` and try again. Also, `key` should actually be the SSH file from `public_key_path` (but without the `.pub` at the end).

At this point, if the project was deployed correctly, you should be able to access the following resources:

- [Airflow Webserver](https://airflow.apache.org) UI at `http://<aws_instance.web.public_ip>:8080`
- [Flask](https://flask.palletsprojects.com) frontend at `http://<aws_instance.web.public_ip>:5000`

>**_Note:_** <aws_instance.web.public_ip> is the final output of the `$ terraform apply ...` command.

Besides the available resources, you may also SSH into the deployed machine at any time:

```bash
# connect to provisioned instance via SSH
$ ssh -i ~/.ssh/key.pub ubuntu@<aws_instance.web.public_ip>
```

In case you are having problems, you may want to look at [Hashicorp's Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs).

#### Wrapping up

Once you're done, you may remove what was created by `terraform apply`:

```bash
# change current working directory
$ cd terraform

# destroys the Terraform-managed infrastructure
$ terraform destroy
```

### Docker

Considering that the stack is organized as a [Docker swarm](https://docs.docker.com/engine/swarm/key-concepts/) stack, the following dependencies must be installed:

- [Docker](https://docs.docker.com/get-docker/)

>**_NOTE_**: If you're using a Linux system, please take a look at [Docker's post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)!

#### Setup

Once you have `Docker` installed, build the Docker images of the services used by the stack:

```bash
# builds services' docker images
$ make docker-build
```

>**_NOTE_**: In order to build **development** images, use `$ make docker-build-dev` command instead!

Finally, update the `env.d` files for each service with the appropriate configurations, credentials, and any other necessary information.

>**_NOTE_**: in order to generate a [fernet key](https://airflow.readthedocs.io/en/stable/howto/secure-connections.html) for Airflow, please take a look [here](https://beau.click/airflow/fernet-key).

#### Initialize Swarm mode

In your deployment machine, initialize Docker Swarm mode:

```bash
# joins the swarm
$ docker swarm init
```

> **_Note:_**  For more information on what is Swarm and its key concepts, please refer to [Docker's documentation](https://docs.docker.com/engine/swarm/key-concepts/).

#### Deploying services

Now that the deployment machine is in swarm mode, deploy the stack:

```bash
# deploys/updates the stack from the specified file
$ docker stack deploy -c compose.yml cs-data-ingestion
```

#### Verifying the Stack's Status

Check if all the services are running and have **exactly one** replica:

```bash
# list the services in the cs-data-ingestion stack
$ docker stack services cs-data-ingestion
```

You should see something like this:

```text
ID                  NAME                            MODE                REPLICAS            IMAGE                               PORTS
ipsdstxfvnpl        cs-data-ingestion_frontend            replicated          1/1                 cs-data-ingestion:frontend          *:5000->5000/tcp
```

At this point, the following resources will be available to you:

- [Flask](https://flask.palletsprojects.com) frontend is available at `http://localhost:5000/v1/render/images`

>**_NOTE:_**  In case `localhost` doesn't work, you may try `http://0.0.0.0:<port>` instead.

#### Logging

In order to check a service's logs, use the following command:

```bash
# fetch the logs of a service
$ docker service logs <service_name>
```

>**_NOTE:_**  You may also follow the log output in realtime with the `--follow` option (e.g. `docker service logs --follow cs-data-ingestion_airflow`). For more information on service logs, refer to [Docker's documentation](https://docs.docker.com/engine/reference/commandline/service_logs/).

#### Wrapping up

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
