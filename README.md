# Backend Interview Test
Coding Challenge. You must be here because you want to [review](#review-project) the project.
***
## Overview
This API is a simple RESTful service that allows to manage this very own repository. You can list existing branches, commits of a given branch, commit details of a given commit, create pull requests, and resolve them.
***
## Index
- [Review project](#review-project)
  - [Install project](#install-project)
  - [Clone from GitHub](#clone-from-github)
  - [Environment](#environment)
  - [Run project](#run-project)
  - [API documentation](#api-documentation)
***
## Review project

#### Install project
- Prerequisites:
  - docker (20.10.7 recommended)
  - docker-compose (1.29.2 recommended)
- Ports:
  - The backend api runs on port `8000` by default.
  - The database for reviewing runs on port `5432` by default.

#### Clone from Github
- Clone:
  ```
  git clone https://github.com/manuelurgell/fullstack-interview-test.git
  ```

#### Environment
- Create .env file wit the following contents (default values are also given in .env.default file, feel free to change them):
  ```
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=test
  POSTGRES_HOST=database
  POSTGRES_PORT=5432
  BACKEND_PORT=8000
  BACKEND_STATIC_PORT=8001
  GITHUB_USER_NAME=Manuel Urgell
  GITHUB_USER_EMAIL=manuel.urgell@outlook.com
  ```
  The GITHUB_USER_NAME and GITHUB_USER_EMAIL variables will be used to sign merge commits.
- Optionally, you can add volume variables to set a volume for the containerized application:
  ```
  APP_LOCAL_VOLUME=~/.docker_volumes/flatdigital/media
  APP_CONTAINER_VOLUME=/app/media
  ```
- And, for productive environments, a secret key should be given:
  ```
  SECRET_KEY=
  ```

#### Run project
- Run with docker-compose:
  ```
  docker-compose build
  docker-compose up
  ```

#### API documentation
- When the service is running, either via docker-compose, docker, or locally, you can go to http://localhost:8000/api to see the full API documentation of each and every endpoint declared in the RESTful API.
- From there you can make tests and see the possible inputs and outputs from every endpoint.
