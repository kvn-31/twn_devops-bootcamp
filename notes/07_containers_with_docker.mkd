# Containers with Docker

Docker = virtualization tool

Linux supports docker directly, Windows and MacOs need docker desktop

## Containers

container = way to package an application with all necessary dependencies and configurations; portable artifact; can be easily shared and moved around;

most containers are linux-based

container repository = storage for containers; mostly private repos for companies, but also public repo for docker (dockerhub)

### Benefits

Before containers:

- most services where installed on OS directly; installation process was different on each OS environment and many steps where needed
- deployment: configuration on the server needed; dependency version conflicts
- dev and ops team had different areas and misunderstandings led to problems

With containers:

- own isolated environment, everything packaged there; one command to install app
- deployment: simplified; dev & ops working together; no envrionmental config needed on server (except docker runtime)

### Container vs Image

Container is made out of images

- mostly base is a linux base image
- application image (f.e. postgres) sits on top
- those layers are downloaded separately -> benefit: no re-download if it is already used in another container

#### Image

- the actual package
- artifact that can be moved around
- contains configuration, layers, start script
- can be found on DockerHub
- consists of various layers

#### Container

- the running environment for an image
- when an image is pulled to a system and started
- container environment is started
- has a port
- virtual filesystem
- data is lost on recreation on default -> need to use volumes


### Docker vs Virtual Machine

The difference lays in the layer, they virtualize.

An OS consists of a Kernel (f.e. Linux) and an Application Layer (f.e. Ubuntu, Manjaro, ...) that sits on top
  
- Docker virtualizes the Application Layer: contains the OS application layer & services and apps installed on top of it
- VM has Applications Layer and its own Kernel -> virtualizes the complete OS

Conclusion
- Docker images are smaller
- Docker containers run much faster
- Docker containers are not compatible with any OS, they only run on Linux, because the Linux Application Layer in a container needs Linux OS Kernel to run
- Docker Desktop makes it possible to run linux-based containers on Windows and MacOs, by using a hypervisor layer with a lightweight Linux distribution


## Docker Architecture

Docker engine gets installed, consisting of:

- Docker Server: pulling images, managinge images & containers
- Docker Api: interact with docker server
- cli: execute commands

### Docker Server

- container runtime: pulling images, managing container lifecycle
- volumes: persist data
- network: container communication
- build images: to build own docker images

## Docker Network

Inside the same Docker Network applications can talk to each other using the container names

--> f.e. JS applications can to be dockerized and join the same docker network

docker network ls -> see docker networks
docker network create NAME -> create a docker network


docker run -d --network twn_course -p 27017:27017 --name mongodb \
	-e MONGO_INITDB_ROOT_USERNAME=admin \
	-e MONGO_INITDB_ROOT_PASSWORD=password \
	mongo

docker run -d -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=password --net twn_course --name mongo-express -e ME_CONFIG_MONGODB_SERVER=mongodb mongo-express 


## Docker compose

- Map multiple docker containers in one file
- by default, sets up a single network for the app
- can also be specified via network key

restart: always -> always restart if it stops (f.e. if mongo express starts first and needs mongo -> will restart and work), also depends_on can be used for this case


## Dockerfile

- blueprint for building images
- starting with a base image (FROM node f.e.)
- configure env variables using ENV (but better be done in docker compose)
- WOKRDIR -> set default dir that commands are executed in
- RUN -> execute any linux command
- COPY -> copy files; executes on Host machine!
- CMD -> executes entrypoint linux command

### Docker build

docker build -t my-app:1.0 .

-t -> tag
. -> directory of dockerfile

### Docker with Jenkins

- app including dockerfile is commited to git
- Jenkins uses this to build the image
- Jenkins then pushes it to Docker repository

## Private Docker Repository (AWS)

- using Amazon ECR (click on private repo "view push commands" for copy paste)
- first of all -> correct aws cli setup is needed
- then login in docker (needed once) aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin BLABLA.amazonaws.com
- naming in docker registries: registryDomain/imageName:tag -> docker.io/library/mongo:4.2
- -> to be able to push to our private registry we need to tag our image first correctly: docker tag my-app:latest BLABLA.amazonaws.com/my-app:1.0; -> this will create a copy of the image with a different name
- then push: docker push BLABLA.amazonaws.com/my-app:1.0

### AWS Setup
- enable IAM
- create user in IAM with AdministratorAccess and AdministratorAccess-Amplify (without email etc)
- for this user generate access key in aws
- in bash: aws configure
- enter access key details etc

AWS Access Key ID [None]: BLA
AWS Secret Access Key [None]: BLA
Default region name [None]: eu-central-1
Default output format [None]: json

## Docker volumes

container has a virtual file system -> if container is removed the data is gone

-> need Docker volumes to persist data
- Folder in physical host file system is mounted into the virtual file system of a docker container -> when container writes data it is automatically replicaed in the host file system (and vice versa) 


### Docker run

docker run -v nginx-vol:/usr/share/nginx/html -> first part (to :) is the host volume, second part is host volume
- the host volume can also be left out, then an anoymous volume will be used (automatically created by docker)
- third way: docker run -v name:/var/lib/data -> specifying a name to reference the directory = named volume -> should be used

### In Docker compose

using a named volume

version: '3'
services:
  mongodb:
    volumes:
     - mongo-data:/data/db
     # ...
volumes:
  mongo-data:
    driver: local

### Docker Volume Locations

- Windows: C:\ProgramData\docker\volumes
- Linux & Mac: /var/lib/docker/volumes
- special on mac: we need to enter docker vm with this command to ls the path: docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh 


## Docker Repository on Nexus

- create Docker (hosted) Repo in nexus ui
- edit repository, configure http connector to different to nexus port -> this will open the port (check with netstat -lnpt)
- create role with nx-repository-view-docker-docker-hosted-*
- assign role to new docker user
- expose the port also on the droplet
- nexus -> realsm -> activate docker bearer token
- if only using http -> need to edit docker daemon file sitting in etc/docker/daemon.json and add insecure registries
- docker tag my-app:1.0 IP:8083/my-app:1.0
- docker push IP:8083/my-app:1.0

## Install Nexus as Docker Container (on Droplet)

- create fresh droplet
- apt update
- snap install docker
- https://hub.docker.com/r/sonatype/nexus3#persistent-data -> create volums to persist data -> docker run
- the image already runs with a nexus user, instead of root (good practice, no work needed) -> this depends on the image -> see tags in docker hub to see what is happening


## Docker best pracices

#### Use official docker images as base images
instead of using base operating system and installing packages by yourself, use official images (f.e. node) as base image

#### Always specify the version, avoid latest
-> FROM node:20.0.2

#### Use small base images, if possible
-> saves storage space
-> less security vulnerabilities
-> alpine is a secure, lightweight base image

#### Optimize Caching image layers
- every docker images is based of layers
- use same base image etc from cache
- once a layer changes, all following layers are re-created
- f.e. npm install -> should only be done when package.json changes -> restructure dockerfile to copy package & package lock files, run npm i and after that copy the app files (which always change)

#### Order Dockerfile commands from least to most frequently changing
-> for caching reasons, see above

#### Use .dockerignore
-> save build size / space

#### Make use of "Multi-stage builds"
- allows creating temporary builds, but only keep the final artifact
- helpful to avoid having dependencies that are only needed for building such as JDK, maven, gradle in the final build
- separate build & run stage (see docs)

#### Use least privileged user to run docker container
- if root user runs a docker container, it might have root access on docker host -> security bad practice
- some images such as node already do this, if not do it manually

#### Scan images for vulnerabilities
- run docker scout cves myapp:1.0




## Commands

docker images -> see all images that exist on local machine
docker run IMAGE -> run image in a container
docker run -d IMAGE -> run image in detached mode (in background)
docker run -p 6000:6002 Host:Container port
-- name NAME -> assign a name
docker run also combines pull & start
docker rmi -> removes image
docker ps -> see all running containers
docker ps -a -> see all existing containers
docker stop ID -> stop container
docker start ID -> start container
docker rm -> remove container
docker history IMAGE -> see layers of image
docker scout cves IMAGE -> scan image for vulnerabilities

### Debug

docker logs ID/NAME -> get logs of container by id or name
docker exec -it ID/NAME /bin/bash -> open terminal of a running container
docker exec -u 0 -it ID bash -> enter container with bash as user 0 (= root)
