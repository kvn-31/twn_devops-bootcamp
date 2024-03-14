# 08 - Build Automation with Jenkins

- is needed to automatically test & build application before a new version is released to save time
- instead of doing locally -> a dedicated server handles it
- done automatically with each push: test code -> build automation -> push to repo -> deploy to server = build automation
- Jenkins is one tool to do it
- Jenkins handles the integrations with the various tools using plugins (gitlab, java, docker, nexus, aws..)

## Install Jenkins (Droplet)

- either directly on OS (more effort)
- or with Docker container

### Using docker container

1. apt update & apt install docker.io
2. docker run -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home jenkins jenkins:lts
3. To find initial admin pw -> docker exec -it CID bash (inside the container) or in the replicated volume folder

## Typical Jenkins Roles
- jenkins admin: administer and manage jenkins; set up cluster, install plugins, backup jenkins data
- Jenkins user: create the actual jobs and workflows

## Configure Tools
in order to have access to node/maven etc either

- use jenkins plugins
- install tools directly on server (inside the docker ocntainer when jenkins runs as container)

Maven: installed via tools

### Inside the container
node & node js

- enter the container as root user docker exec -u 0 -it 684b95be2c92 bash
- apt update, apt install curl, curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh -> bash nodesource_setup.sh
- apt install nodejs -> node and npm now available

Alternative: Install the plugin and use as tool

## Create new Job

- Freestyle Job: most simplistic, straightforward, small-scale -> use one job per step (build, test, docker build, push to repo)
- pipeline / multibranch pipeline will normally be used

## Configure Git Repo

In job config, add git repo, add auth and specify branch(es) -> all files will be cloned to /var/jenkins_home/workspace/my-job


## Docker in Jenkins

- Jenkins is running in a docker container on the host -> we want to make the docker runtime on the host available within the Jenkins container by mounting

### create jenkins container with mounted docker
docker run -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home -v
/var/run/docker.sock:/var/run/docker.sock

docker.sock = unix socket file used by docker deamon to communicate with docker client


### enter as root and complete docker installation
docker exec -u 0 -it ID bash
inside: curl https://get.docker.com/ > dockerinstall && chmod 777 dockerinstall && ./dockerinstall

now we need to set correct permissions for docker.sock for jenkins user

chmod 666 /var/run/docker.sock -> Important! This needs to be done after every container deletion

### Docker build in jenkins

- added a dockerfile in root of project
- in jenkins job -> maven package, then in "execute shell" docker build -t java-maven-app:1.0 . 
- java-maven-app can now be found in docker images

### Push images to docker hub

- create a private repository on docker hub (one is free)
- jenkins -> add credentials of dockerhub
- add credentials in job config
- docker build -t kvnvna/demo-app:jma-1.0 .
echo $DOCKERHUB_PW | docker login -u $DOCKERHUB_USER --password-stdin
docker push kvnvna/demo-app:jma-1.0

### Push images to nexus

- add credentials in jenkins
- docker build -t 164.92.238.146:8083/java-maven-app:1.0 .
echo $DOCKERHUB_PW | docker login -u $DOCKERHUB_USER --password-stdin 164.92.238.146:8083
docker push 164.92.238.146:8083/java-maven-app:1.0


### Chain: Freesytyle to Pipeline Job

- use post build actions
- was used before the pipeline type job was created
- limitations: input fields of plugins; not suitable for complex workflows
- -> (jenkins) pipelines got introduced and should be used


## Pipeline Jobs

- benefits vs freestyle jobs
    - can handle user input
    - conditional statements
    - tasks can run in parallel
    - do not rely on plugins
    - lower maintanance costs
- scripted instead of UI
- written with Groovy (similar to Java)
- best practice: pipeline script in Git Repo
- scripted syntax: advanced capabilities, difficult to start
- declarative syntax: easier, not that powerful, pre-defined structure

### Declarative
```
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
```
### Env Variables in Jenkinsfile

- JENKINSURL/env-vars.html provides a list of all available jenkins env vars
- for own env vars: environment {}
- for jenkins credentials using credentials binding plugin: MY_CREDENTIALS = credentials('server-credentials')
- can also be done inside a stage:

```
withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh 'docker build -t kvnvna/demo-app:jma-2.0 .'
        sh 'echo $PASS | docker login -u $USER --password-stdin'
        sh 'docker push kvnvna/demo-app:jma-2.0'
    }
```

### Using envsubst to replace env vars in files
- use case: we have a k8s deployment file with env vars that need to be replaced with values from jenkinsfile
- envsubst needs to be installed in jenkins container
  - exec into jenkins container as root 
  - `apt-get install gettext-base`
- envsubst creates a temporary file with the replaced values, which we can pipe: `envsubst < kubernetes/deployment.yaml | kubectl apply -f -`
- 

### Tools

- specify tools { } block -> makes tool available in all stages
- tools have to be installed in jenkins -> check tools

```  
tools {
        maven "maven-3.9"
}
```
use the name that was created in jenkins tools


### Parameters
```
parameters {
        string(name: 'BUILD_VERSION', defaultValue: '1.0.0', description: 'Version of the build')
}
```

- types: string, choice, booleanParam
- once introduced, it will enable the Build with Parameters in Jenkins

### Script Blocks
- using only one Jenkinsfile for a whole project might lead to a rather long file -> we move parts to external scripts
- all environmental variables are also available in script block


### Input Parameter

- allow users to specify parameters (f.e. which environment to deploy to)
- this will pause the build until the user inputs a value
```
        stage('Deploy') {
            input{
                message "Select the environment to deploy"
                ok "Done"
                parameters {
                    choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Environment to deploy')
                }
            }
            steps {
                echo "Deploying version ${PARAM_BUILD_VERSION}.. to ${ENV} environment"
            }
        }
```

- inside the script tag to assing values to env variables
```
        script {
            env.ENV = input message: "Select the environment to deploy", parameters: [choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Environment to deploy')]
        }

        echo "Deploying version ${PARAM_BUILD_VERSION}.. to ${ENV} environment"
```

## Multibranch Pipelines

- create branches for dev, test, stage
- but also dynamically add for each added feature branch
- create multibranch pipeline job
- filter for branches that should be discovered in branch sources
- make use of built-in variables such as BRANCH_NAME
```
when {
                expression {
                    BRANCH_NAME == 'master'
                }
            }
```

## Credentials in Jenkins
- using the Credentials plugin to manage centrally
- scopes
    - system: only available on Jenkins server -> not accessible by jenkins jobs
    - global: accessible everywhere
    - project: only for multi-branch pipeline; only scoped to project
- types
    - username pw
    - secret file, text
    - certificate, ...
    - can be added by plugins
- id -> used to reference


## Jenkins Shared Library

- application with microservices, multiple projects, ...
- with pipelines:
    - -> build each microservice app
    - -> each microservice would need its own jenkinsfile, but most of the content is the same as in the other microservices -> replication of logic
- Solution: Jenkins Shared Library
    - extension to pipeline
    - own repository, in groovy
    - contains all shared logic in jenkinsfile

### Structure

- vars folder
    - all functions called from jenkinsfile
    - each function in individual groovy file
- src folder
    - helper/utility code
- resources folder
    - non groovy files

### Jenkins Setup
- manage / system / global pipeline libraries
- default version = branch/commit hash/tag
- alternative: reference directly in jenkinsfile if lib is not needed for all jenkins projects
```
library identifier: 'jenkins-shared-library@master', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/kvn-31/twn_jenkins-shared-library.git',
   credentialsId: 'github-credentials']
)
```

### Project Setup
in the actual project we need to import the library, which was specified in jenkins

Jenkinsfile:
```
#!/usr/bin/env groovy
@Library('jenkins-shared-library')
```
now we can use the provided functions

```
stage("build jar") {
            steps {
                script {
                    buildJar()
                }
            }
        }
```

### Parameters in Shared Library
Parameters can be added to a function in the shared lib (such as a image version) and then specified in the projects call to the function


### Extract logic to src (utility)

groovy file
```
import com.example.Docker

def call(String imageName) {
    return new Docker(this).buildDockerImage(imageName)
}
```

Docker.groovy in com.example package
```
#!/usr/bin/env groovy
package com.example

class Docker implements Serializable {

    def script
    Docker(script) {
        this.script = script
    }

    def buildDockerImage(String imageName) {
        script.echo "building the docker image with name $imageName..."
        script.withCredentials([script.usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
            script.sh "docker build -t $imageName ."
            script.sh "echo '${script.PASS}' | docker login -u '${script.USER}' --password-stdin"
            script.sh "docker push $imageName"
        }
    }
}
```

## Trigger Jobs automatically

- manually is good for production release
- to automatically trigger pipeline when changes happen in r epo webhooks of SCM need to be setup
- jobs can also be scheduled, for example for long running tests
- add SCM plugin if needed (Gitlab f.e.)


### Github
- using the pre-installed github plugin
- in github: generate personal access token with admin:org_hook; then for the project add a webhook with payload url (needs to match jenkins later, default is http://IP/github-webhook/) and application/json, secret empty
- in jenkins: global config -> Github servers -> add with credentials access token as secret text
- now move to the pipeline configuration an set a tick for Github hook trigger for GITScm polling

### Gitlab
- Install Gitlab plugin
- once installed -> in system config Gitlab configuration is added
- default host url is https://gitlab.com/
- for api token -> click on add -> gitlab api token -> generate api token with scope api in gitlab
- in the job -> set gitlab connection, enable build trigger Build when a change is pushed to gitlab
- in gitlab: project -> integrations -> Jenkins -> Enable & Trigger push, specify jenkins url, job name and user pw

### For multi-branch pipeline
- will need another plugin -> multibranch scan webhook trigger (when using gitlab)
- for github it should work if the branch source is done using Github, NOT Git
- gitlab:
    - install multibranch scan webhook trigger plugin
    - inside the job -> enable scan by webhook
    - trigger token -> give name
    - in gitlab: open webhook
        - url: copy partly from help section of the plugin, replace with correct url; add gitlabtoken name at end
        - push events

## Dynamically increment application version
- https://github.com/kvn-31/twn_java-maven-app/tree/increment-app-version
- common approach to naming: x.y.z-suffix -> major.minor.patch-suffix
- version push should normally done automatically in build automation
- each build tool, works differently, but have tools to increment version
    - maven for patch version: mvn build-helper:parse-version versions:set -DnewVersion=\${parsedVersion.majorVersion}.\${parsedVersion.minorVersion}.\${parsedVersion.nextIncrementalVersion} versions:commit
- command needs to be executed by jenkins, can be done in a dedicated stage
- it is important to also secure that only the right version is used in the COPY and ENTRYPOINT command in dockerfile -> this can be done by doing a mvn clean package which removes all other builds and a regex for copy command
- important: the version bump up needs to be done in both: jenkins and the repository! -> commit & push needs to be done after version bump -> we need to ignore those commits in jenkins webhook (otherwise a loop of commits is created)

### Ignore commits by specific user
- to avoid the problem of a loop of commits, we need to be able to avoid pipeline triggering for specific user
- install Ignore Committer Strategy plugin
- set in jobs build configuration


## Pretty helpful: Pipeline script generator
- click on a pipeline, then on pipeline syntax -> use the tool

