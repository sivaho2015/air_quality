# Data engineering project: air quality data extraction to analysis

Fetch real-time air quality data using aqicn.org API and load the data into a PostgreSQL warehouse. Use dbt to transform data and create dimension and fact tables.
Metabase is then used to do analysis on air quality in the US and create a dashboard.

# Architecture diagram

![Architecture] (https://github.com/sivaho2015/air_quality/blob/main/assets/images/arch_diagram.png?raw=true)

# Dagster data pipeline

![Pipeline] (https://github.com/sivaho2015/air_quality/blob/main/assets/images/pipeline.png)

# Metabase dashboard

![Dashboard] (https://github.com/sivaho2015/air_quality/blob/main/assets/images/dashboard.png)

## Setup

### Pre-requisites

1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/) with at least 4GB of RAM and [Docker Compose](https://docs.docker.com/compose/install/) v1.27.0 or later

Run these commands to set up the project locally.

```shell
# Clone the code as shown below
git clone https://github.com/sivaho2015/air_quality.git
cd air_quality

# Local run & test
make up # start the docker containers on your computer
make ci # runs auto formatting, lint checks, and all test files under ./tests
```

### Tear down infra

Run these commands to tear down infrastructure

```shell
make down # stop docker containers on your computer
```

## References

1. [Dagster docs](https://docs.dagster.io/tutorial)
2. [Metabase docs](https://www.metabase.com/learn/getting-started/getting-started.html)
4. [Dagster docker setup](https://github.com/dagster-io/dagster/tree/0.14.17/examples/deploy_docker)
5. [dbt docs](https://docs.getdbt.com/)