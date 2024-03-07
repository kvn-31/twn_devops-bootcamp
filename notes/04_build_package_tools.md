# Build & package manager tools

Application is packaged in a single movable file = application artifact
packaging = building the code -> compiling, compressing, hundreds to one file

artifact can be deployed multiple times, backed up, multiple envs, ..


Artifact repository -> artifact is kept there for multiple uses (f.e. Nexus, JFrog Artifactory)

Process: New version of application is created -> artifact is built -> save articat to artifacte repostiory -> deploy to server

Java -> JAR or WAR (JAR = Java Archive) = whole code plus dependencies

## Build Artifact
- using build tool, depending on programming language (maven with xml or gradle with groovy)
- installs dependencies, compiles and compresses code

gradle build or mvn install

## Dependencies
- build tools are also needed locally for developing the app
- Dependencies file -> manages dependencies for project (pom.xml, build.gradle)
- dependencies come from respective repositories
- gradle & maven -> add dependency and refresh project in intelliJ

## Run application

java -jar NAMEOFJARFILE

## Differences for node.js
- zip or tar file
- no special artifact t ype
- npm & yarn using package.json
- npm & yarn are package managers, no build tools
- zip/tar file includes applicaiton code but not the dependencies -> to run the app on server the dependencies must be installed first -> copy artifact & package.json (can be both in one file)
- npm pack -> packages whole application (no build)
- npm start -> start application
- in JS world more flexible, not as structured and standardized

## Handle different FE & BE
-> can be done in separate files or common artifact file
example: FE in React, BE in Node.js
-> separate package.json or one common package.json
React needs to be transpiled (jsx not understood  by  browser yet)

### Webpack - build tool
widely used build tool for js
transpiles, minifies, bundles, compresses the code

### Python
Pip package manager

## All in common
- dependency file (pom.xml, ..)
- repository for dependencies
- command line tool
- package managers (gradle, npm, pip, ..)

## Publish an artifact
after building we need to publish/push our artifact to the artifact repository (f.e. nexus). after that we can fetch it from anywhere from the repository

## Build tools and docker
- with Docker we have just one artifact type -> docker image
- Docker images instead of zip/tar artifacts are built
- also only one repository is needed (for docker images)
- dependencies can be installed inside the docker image
- Docker image is an artifact -> alternative for all other artifact types
- no npm or java needed on the server -> can be executed in the image
- applications still need to be build (f.e with webpack)

example
FROM node:10 AS ui-build
WORKDIR /usr/src/app
COPY my-app/ ./my-app/
RUN cd my-app && npm install && npm run build

FROM node:10 AS server-build
WORKDIR /root/
COPY --from=ui-build /usr/src/app/my-app/build ./my-app/build
COPY api/package*.json ./api/
RUN cd api && npm install
COPY api/server.js ./api/

EXPOSE 3080

CMD ["node", "./api/server.js"]

## Build tools as DevOps engineer
Devs -> configure dependencies
DevOps -> helps to build the application (artifact) -> knows where and how to run on server
normally a build automation / ci cd pipeline is setup: install dependencies, run tests, build/bundle app, push to repo

tests need to be executed on the build servers











