# Container that installs Python requirements and performs auto formatting, testing, type checks, and lint checks
FROM python:3.9.5

# set up location of code
WORKDIR /code
ENV PYTHONPATH=/code/app

# install python requirements
ADD container/formatter/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy repo
COPY ../../ /code/

# entry point for formatter container
ENTRYPOINT ["tail", "-f", "/dev/null"]