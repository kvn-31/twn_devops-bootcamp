# Artifact Repository Manager

## Definition
Artifacts = apps built into single file
Artifacts Repository = where to store those artifacts
Artifacts Repo Manager -> Artifacts produce different types -> different repositories needed (e.g. one for jar, one for python, ..) -> easier way: one application to manage all -> f.e. Nexus/Jfrog

Public Repository Manager = f.e. Maven Repo, Npm, ..


## Nexus
- Artifact Repository Manager
- Upload and store different build artifacts
- Retrieve artifacts later
- central storage
- for internal (f.e. company use)
- also a proxy for public repository can be created (to be able to also fetch public artifacts from nexus)
- can integrate with LDAP
- provides REST API to integrate with other tools (f.e. ci/cd)
- backup & restore
- metadata tagging
- cleanup policies
- search functionality
- user token support for system user authentication

## Setup Nexus

We need a droplet that satisfies our requirements (research before)

1. Install java 8 -> apt install openjdk-8-jre-headless
2. cd /opt
3. copy the unix archive link from sonatype page
4. wget URL -> download the package
5. tar -zxvf FILENAME -> untar the package -> we now have two folders
6. best practice: create own nexus user
7. set user in nexus rc -> vim nexus-3.64.0-04/bin/nexus.rc -> uncomment line and set user
8. /opt/nexus-3.64.0-04/bin/nexus start -> start nexus
9. open the port (8081) to public
10. the admin password can be found with cat /opt/sonatype-work/nexus3/admin.password

## Nexus Folders


#### Nexus folder
- with runtime and application of nexus
- will be overwritten in an update

#### sonatype-work folder
- config and data
- logs, metadata, artifacts
- used to backup

## Nexus UI

### Repository Types

#### Proxy Repository
linked to a remote repo -> to a public repository like maven

if we look for a component, nexus will scan if component is available locally, if not the request will be forwarded to remote repo -> downloaded and cached -> for next time it is available

Advantage:
- Saves network bandwith
- single repository endpoint for everything

#### Hosted Repository
- primary storace for artifacts and components (f.e. company artifacts)
- f.e. all artifacts developed by company stored there
- best practice: development version added to snapshot version; if ready to release -> added to releases (f.e. maven-snapshots, maven-releases)
- maven-releases can also be used for 3rd party libs that are not publicly available
- maven-snapshots for internalt development versions

#### Group Repository

allows to combine multiple repositories and even repository groups in a single repository -> single url for multiple repositories

### Create Nexus user

Normally we can do this with LDAP, but we can also manually add users via settings - users

Best practice is to do a granular permission management

## Push Maven/Gradle artifact to Nexus

### Gradle
set publishing -> publications & repositories in build.gradle (see project in folder)

Authentication is done via referencing in settings.gradle (not checked in!)

By adding apply plugin: 'maven-publish' in build.gradle we enabled to use gradle publish
-> this will use the specified settings and publish to nexus

### Maven

Need to add publishing plugins to pom.xml, specify location of nexus in distributionManagement

Authentication is done via -m2 folder in local system

-> cd ~/.m2 -> create settings.xml (google for structure)

mvn deploy -> uploads jar to nexus repo


## Nexus API

mostly used for ci/cd pipelines

List all repositories (that user is allowed to see)
curl -u user:password 'IP:PORT/service/rest/v1/repositories'

List all components in certain repo
curl -u user:password 'IP:PORT/service/rest/v1/components?repository=maven-snapshots'


## Blob Storage

- Nexus uses blog storage for its components
- storage mechanism for binary files of artifacts
- can be local or cloud (s3 f.e.)
- manage via settings/blob stores
- types: file system-based storage vs S3 (AWS)
- once created -> cannot be modified, if used by repo it cannot be deleted
- -> decide carefully which size is needed
- can be assigned to repository, cannot be changed

States:
- started = running as expected
- failed = failed to initialize

## Component vs Asset

- in Browse -> we see in tree like structure the JARs,.. we uploaded
- top-level folders are the components
- files below are assets that belong to a single component
- component: abstract, high level; can be docker image, zip file, jar file, ..
- asset: actual files/packages
- Docker gives assets unique identifiers = Docker Layers
- f.e.: 2 Docker images -> 2 Components, but share same assets

## Cleanup policies

- Create & assign to repositories
- we can use the preview which snapshots would be deleted
- when assigned, nexus will schedule a cleanup task -> see settings/system/tasks
- those files will not be permanently deleted, but marked for deletion = Soft Delete
- to actually delete those items, we need to create task: Admin - compact blob store
- to test: manually execution can be done clicking on the task and "run"

## Install Nexus as Docker Container (on Droplet)

- create fresh droplet
- apt update
- snap install docker
- https://hub.docker.com/r/sonatype/nexus3#persistent-data -> create volums to persist data -> docker run
- the image already runs with a nexus user, instead of root (good practice, no work needed) -> this depends on the image -> see tags in docker hub to see what is happening











