# Checkout and install dagster libraries needed to run the gRPC server
# exposing repository to dagit and dagster-daemon, and to load the DagsterInstance

FROM python:3.7-slim

# Install dependent packages
RUN pip install --upgrade pip
RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker \
    requests \
    psycopg2-binary \
    dagster-dbt \
    dbt-core \
    dbt-postgres \
    flatten_json

WORKDIR /opt/dagster/app
ENV PYTHONPATH=/app

# Copy files in app to dagster app directory
COPY ../../app /opt/dagster/app/

# Run dagster gRPC server on port 4000
EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that
# want to run other commands against the repositoy
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repository.py"]