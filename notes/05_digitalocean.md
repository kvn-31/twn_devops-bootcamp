# 05 cloud & infrastructure as service with DigitalOcean


## Infrastructure as a service
- web app needs to run somewhere -> we need jenkins on a server

either: company buys own servers, has dedicated team, needs to fix issues, ..

or (better): Infrastrucutre delegated to cloud company; all physical infrastructure moved to cloud; just rent servers

IaaS = move from on-site/on-premise infrastrucute to cloud providers

AWS/Google Cloud/Azure/DigitalOcean


## Droplet
by default - all ports are publicly open -> bad security practice
-> first step: configure firewall

### Firewall
navigate to droplet -> network -> firewall -> create / set firewall rules
-> leave port 22 open for ssh -> but under sources set your ip adress/something like that

### Copy files to server

we built the jar file for a java project using gradle build, now we move it with scp

scp build/libs/java-react-example.jar root@165.22.81.223:/root (the :/root states the path where we want to copy it to on the server)

start on the server
java -jar java-react-example.jar

#### Expose Port on firewall

Add rule on digitalocean
custom - tcp - port - all ipv4 ipv6

we can now access it ip:port

Useful:
ps aux | grep java -> find all running java applications

netstat -lpnt -> list all servers with active internet connections -> see the port

## Create and configure a linux user on cloud server

Security best practice -> do not start appliactions with root -> each application has its own user

adduser archie
usermod -aG sudo archie // add user to sudo group
su - archie // switch to new user

### Directly connect to specific user on server using ssh (Add ssh key)

switch from root to new user on server
copy the public key from the local user (on my machine)

on server:
mkdir .ssh (in home directory of the archie user f.e.)
sudo vim .ssh/authorized_keys
paste the public key and save

now we can:
ssh archie@ip