
## Pre-requisites
- Having an application (in our case nginx) running on a server.
Linode server with debian, installed docker, started nginx container.
  - linode api token
- having an email to send notifications
  - in this case: gmail address with app password
- email details in environment variables (can be done in intellij for testing)
  - `EMAIL_ADDRESS`
  - `EMAIL_PASSWORD`
  - `DEBIAN_ROOT_PW` -> to login to the server (only needed if set)
  - `LINODE_API_TOKEN` -> to interact with linode api


## Goal
We have a simple nginx application running on a server. We want to monitor the website and send an email if the website is down.
In addition, we want to automatically restart the docker container or the whole server if the website is down.

