# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install pipx and poetry
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y python3-venv curl \
    && apt-get -y install netcat gcc postgresql \
    && pip install --user pipx \
    && /root/.local/bin/pipx ensurepath \
    && /root/.local/bin/pipx install poetry==1.8

# add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# copy local wheel file
COPY PyYAML-5.4.1-cp39-cp39-macosx_10_9_x86_64.whl ./

# copy Poetry files
COPY pyproject.toml poetry.lock ./

# install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]