# first play
apt update
apt install openjdk-8-jre-headless
apt install net-tools

# second play
cd /opt
wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz
tar -zxvf latest-unix.tar.gz

# third play
adduser nexus
chown -R nexus:nexus nexus-3.28.1-01
chown -R nexus:nexus sonatype-work

# fourth play
vim nexus-3.28.1-01/bin/nexus.rc
run_as_user="nexus"

su - nexus
/opt/nexus-3.28.1-01/bin/nexus start

# fifth play
ps aux | grep nexus
netstat -lnpt
