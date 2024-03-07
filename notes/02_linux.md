02 - Linux

Tasks of OS

Process = Small Unit that executes on a computer; e.g: new browser tab, starting intelliJ
has own isolated space
1 core CPU -> One Process at a time

Memory Management -> RAM = Working Memory
Memory Swapping -> OS swaps memory between applications; one app becomes inactive, new one gets resources, slows down computer
-> Swap-out memory and save to storage for Procces 1 and swap in RAM for Process 2

Storage Management = Secondary Memory -> persisted; can be loaded into RAM again.

File System
Unix Systems (f.e. Linux) -> tree file system
Windows: still hierarchical, but multiple root folders

Management of IO devices

Security (f.e. User Permissions)

Networking

__

Core of OS is the Kernel -> loads first; Heart of System; manages hardware components

On Top of Kernel: Applications Layer (f.e. Ubuntu, Manjaro,..)
MacOs / iOS based on Darwin

Interact with Kernel over GUI or CLI (f.e. in Server Operating Systems)

Hardware -> Kernel -> Application Layer -> Applications

MacOs is built on top of UNIX -> Standarsds were created (POSIX)
Linux was developed parallel to UNIX but followed the same philosophy (unix-like)
Linux and MacOs are POSIX compliant -> Similarities

__

Virtualization

Hypervisor -> VirtualBox (open-source)

Type 1 Hypervisor = works same as type 2, but hypervisor is installed directly on the hardware (=Bare Metal Hypervisor); vmware ESXI, Microsoft Hyper-V;
Once installed concept is the same -> One Physical Server with Bare Metal Hypervisor on it -> Multiple Guest OS Sharing resources
Used by cloud providers such as AWS; efficient usage of hardware resources; users can choose resource combinations; Abstracting away the OS from the Hardware itself -> OS as portable file -> with virtualization it is fail safe because backups can be done -> Snapshot
Type 2 Hypervisor = create VM on top of host OS; borrow resources from host OS -> for personal use

__


Linux File System

one root folder; hierarchical

/home -> home directories for all users
/root -> home directory for root user


/bin -> binary executables for most essential user commands (f.e. cat); available system-wide

/sbin -> system binaries; commands that are system relevant and need SU permission

/lib -> hold libraries for the binaries/commands

/usr -> was user location before /home was added; also has /sbin, /bin, /slib, ... has same commands as /bin folder -> historic reason (to save space), concept remains -> commands are usually executed on usr/bin


/usr/local -> location for programs the user installed (system-wide)

/opt -> for applications that install everything in one directory instead of splitting between /bin, ... f.e. IDE


/boot -> files required for booting (do not touch lol)

^ all those are read-only (install but never touch again)

/etc -> configurations

/dev -> devices; location of device files (accessed by apps/drivers)

/var/log -> variable = log folder
/var/cache 

/temp -> for temporary files for different applications

/media  -> external drives are mounted here

/mnt (mount) -> to manually mount a file system use the mount folder


hidden files -> start with . -> (mostly) automatically created by apps/os

__

CLI

username@computername(or hostname in servers) ~$
~ = home directory (home/username)
$ = regular user
# = root user

pwd = print working directory
ls = list folders and files
ls /etc/network -> display content of etc/network
ls -R Documents -> display contents of folders recursively
ls -a -> display also hidden files
cd [path] = change directory
cd / got to root folder
mkdir [name] = make directory
touche [filename].[extension] = create file
rm [filename].[extension] = delete file
rm -r [path] = recursively remove (for folders)

In Linux everything is a file -> also folders are represented as a file, also commands, devices, ..

Navigating through file structure
Absoulute path cd /myPath
go two levels back cd ../..

mv = move
mv web-application java-app -> renamed the folder
cp = copy
cp -r java-app my-project copies to new folder (-r = recursive and needed for folder contents)
cp file.txt file-new.txt -> copies to new file

history -> displays all commands executed in this session (saved in .bash_history)
history 10 -> last 10 commands
CTRL + R -> searches through executed commands

cat = concatinate -> display file contents
cat Documents/java-app/Readme.md

cat /etc/issue -> find out which Distribution

Display OS specifications

uname -a -> all info about kernel/system
cat /etc/os-release -> which distribution/version..
lcspu -> info about CPU
lsmem -> info about memory

to execute one command as root -> sudo

sudo adduser username -> adds a new user
su - admin -> switch user to admin

__

Package Manager

Windows: all files in one folder
Linux: spread across folders (bin, lib, ..)
Dependencies are often needed -> those are reasons to use a Package Manager

Downloads, installs and updates from a repository
Ensures authenticity
Resolves required dependencies
Knows where to put / remove the application files

APT - Advanced Package Tool (<- example PM)

apt search openjdk / pacman -Ss opendjdk -> search packages

sudo apt install package_name / pacman -S package_name -> install package(s)
sudo apt remove package_name
pacman -R package_name -> remove without dependencies
pacman -Rs package_name -> remove with dependencies that are not needed by other packages

sudo apt update -> refresh package database

APT-GET

search not available
more specific output
can achieve the same but with additional command options

conclusio: apt more user friendly


Packages are coming from different repositories, to see which ones are used: cat /etc/apt/sources.list


Alternative Ways to install
- if package is not available/outdated

f.e.: Ubuntu Software Center
Snap Package Manager: difference -> all dependencies are included in one bundle (self contained) -> larger size

snap list -> list all snap packages
sudo snap refresh -> update al snap packages (should normally be done automatically once per day per default)

Which one to use? if possible use apt/pacman, if not Snap


Add another repository to the list
- needed for installing rather new applications which are not in official repositories yet
- will be added to /etc/apt/sources.list
- apt install will look in all repositories in sources.list

PPA = Personal Package Archive -> provided by community
-> possible risks, verify yourself


Generally Linux: Debian (Ubuntu, Debian) -> Apt vs Red Hat Based (CentOs, Fedora) -> Yum Package Manager

__

Vim Editor

Vi
Vim (improved version)

create and edit at same time
fast (especially in cli)
support multiple formats
when working on remote server

vim filename -> open file or open a new file

two modes
- Command Mode (default): cannot edit text, navigate, delete, searche, ...
- Insert Mode: Enter Text
To switch: i
To go back: ESCAPE

:wq -> quit vim :joy:
:q! -> discard and quit

dd -> remove line
d10d -> remove 10 lines#
u -> undo change
A -> jump to end of line and switch to insert mode
0 -> Jump to beginning of line (stay in command mode)
$ -> jump to end of line
24G -> jump to line 24
/bla -> search (for bla in this case)
n = jump to next match
N = jump to preverious match
:%s/old/new -> replace old with new throughout the file

__

### Linux Accounts & Groups

User Categories

- Superuser: root - unrestricted permissions; 1 per system
- User Account: regular user; own dedicated space in /home
- Service Account: Relevant on Server Distros. earch service (f.e. Msql, Apache,..) has its own user = Best Practice

Windows: users can be managed centrally; user only sees own folder; centrally managed user permissions -> login to any hardware connected to system
Linux: Users managed on that specific hardware -> only on one computer; Multiple users is relevant for servers

Every user should have his own account:
- permission management
- who did what? traceability

#### User Permissions / Groups

- per user
- per group -> best way (f.e. Dev, DevOps, Admin,.. group)

/etc/passwd file -> stores user account information

archie:x:1000:1000:archie:/home/archie:/bin/bash
username:password:uid:gid(groupid):gecos(user info):homedir:default shell 

sudo adduser tom / for arch: useradd -m archie
by default adds user group with username

passwd tom -> set new password for user
su - tom -> bash switch to tom user
su - -> login as root user

sudo groupadd devops -> add new group
sudo delgroup devops -> remove devops group

adduser and addgroup vs useradd and groupadd
easer to use if available vs for automated way

sudo usermod -g devops archie -> put archie in devops group (user can have multiple secondary groups)
sudo usermod -G devops,othergroup archie -> sets archie to secondary groups -> overwrites secondary group list
sudo usermod -aG newgroup archie -> append newgroup to user secondary group list

groups -> display all groups of current user
groups archie -> groups of archie user

sudo gpasswd -d archie devops -> removes archie from devops g roup

#### File Permissions

ls -l -> shows permissions for file
ls -la -> for hidden files as well


Ownership: which user & which group own file/folder (usually the user who created it, group is the primary group of user)

chown -> change ownership
chown archie:admin Readme.md -> change ownership of readme to user archie and group admin

chown archie Readme.md -> change ownership to user
chgrop group Readme.md -> change ownership to group

-rw-r--r-- 1 archie archie 164  9. Jän 15:24 devopsbootcamp.md
type/permission/etc user group ...


d -> directory
- -> regular file
c -> c haracter device file
i -> symbolic link

r -> read
w -> write
x -> execute
- -> no permission

drwxrwxr-x 2 user group
d: directory
rwx: first block of permissions for user (rwx)
rwx: second block of permissions for group (rwx)
r-x: permissions for everybody else (not user or group member)

#### Modifying permissions

chmod -x api -> take away execute permissions for api folder for all owners
chmod g-w config.yaml -> remove write for group (-)
chmod g+x config.yaml -> add execute for group (+)
chmod u+x script.sh -> add execute to user
chmod o-x script.sh -> remove execute for others

u/g/o = user/group/other
+/- = add/remove
r/w/x = read/write/execute

Change multiple permissions for one owner

chmod g=rwx config.yaml -> add rwx to group
chmod g=r-- config.yaml

With numeric values
0 ---
1 --x
2 -w-
3 -wx
4 r--
5 r-x
6 rw-
7 rwx

chmod 777 script.sh -> everybody has rwx permission

sudo chmod 740 script.sh -> user all; group read; others nothing

__

#### Pipes and Redirects

The output of one program can become input of another command

Pipe | and less

cat /var/log/syslog -> logs a lot
cat /var/log/syslog | less -> less displays in a more userful manner
ls /usr/bin | less -> page by page view -> next page by spacebar; q to quit; b to prev page


Pipe and Grep

history | grep sudo -> global search for regex and print out -> any commands that has sudo in it
history | grep "sudo chmod" -> for multiple words

Multiple Pipes

history | grep sudo | less

#### Redirects >

history | grep sudo > sudo-commands.txt -> saves the output to a file

cat sudo-commands.txt > sudo-rm.txt -> all contents copied to another file

history | grep rm >> sudo-rm.txt -> append (>>) content to existing file

Every programm has 3 streams
STDIN(0) = Standard Input
STDOUT(1) = Standard Output
STDERR(2) = Standard Error

#### Separate commands in one line ;

clear; sleep 1; echo "Hi" -> independently executed one after another

__

### Shell Scripting

-> to run multiple commands in the same order
-> avoid repitive work, keep configuration, share instructions, logic/bulk operations

Shell vs Bash

Shell interpretes and executes various commands -> translates our command so that OS Kernel understands it

.sh (Bourne Shell) -> used to be default shell
Bash (Bourne again shell) -> improved version of sh; currently default shell program for most unix like systems

Shell & Bash share the same extension (.sh)
We tell which to use by specifiying on top

Shebang (# = sharp; ! = bang -> short = shebang)
#!/bin/bash -> use bash
#!/bin/sh -> use Bourne shell

#### Variables
file_name or fileName

file_name = config.yaml
echo "using file $file_name"

Store output of command in variable
variable_name = $(command)
config_files = $(ls config)


#### If Else (conditionals)

if [ -d "config" ] -> folder config exists?
then
    echo "reading contents"
    config_files=$(ls config)
else
    echo "no config dir, creating one"
    mkdir config
fi
_
elif -> else if
_
echo "contents of config folder $config_files"
_
if [ "$user_group" == "admin" ] ...


For Bash double brackets are used -> improved version with more features
[ -> POSIX
[[ -> BASH 


File Test Operators
-d -> is a directory?
-f -> is a file?
-r -> readable?
...

-gt -> greater than
...

= -> POSIX Standard
== -> Bash specific
...

#### Params
Positional Parameter -> Arguments are processed in same order theyre sent
Indexing starts at 1

user_group=$1
./shellscript.sh value
-> user_group = value

$* -> represents all params in a string
echo "all params $*"

$# -> number of params provided

_
(testShell2.sh)

#### User Input

read -p "Please enter username" user_name
echo "Username is $user_name"

#### Loops

wile, for, until, select

for param in $*
 do
   echo $param
 done


while true -> indefinite loop
while true
do
	read -p "enter a score" score

	if [ "$score" == "q" ] 
	then
		break
	fi
	sum=$(($sum+$score)) --> arithmetic needs parenthesis
	echo "total score: $sum"
done

___

(testShell3.sh)
### Shell Functions

function score_sum { <-- define function
...
}
score_sum <-- call function

Dont use more than 5 parameters per function -> small chunks of code -> split

function create_file() {
	file_name=$1
	is_shell_script=$2
    #...
}

create_file test.txt true

Return values

function sum() {
	return $(($1+$2))
}

sum 2 10
result=$? #<-- capture value returned by last command

___

### Environment Variables

each user -> own environment; preferences
OS configurations should be separted from user environments

key value pairs that store information and are available for the whole environment

name UPPER_CASE
USER=archie
HOME=/home/archie

printenv -> list all env variables
printenv USER -> print specific env variable
printenv | grep USER -> print all env variables with USER (f.e. USERNAME)
echo $USER -> reference by $

####Environment Variables in Applications
Example: App -> needs key/token to access an api -> how are they stored?
common way: Set data as env vars on server -> apps can read those
DB_PWD=secret

Use Case: Make application more flexible

Dev vs Testing vs Production Stage
-> all have own DB -> own credentials -> dynamically replaced & flexible

####Create env variable

export DEMO_ENV_VAR=value -> set / change value
unset DEMO_ENV_VAR

when set with export command in command line interface -> only set for this specific session!

#### Set Permamently (for user)
in .bashrc file -> shell configuration file -> per user shell specific configuration

reload the file to refresh after changes -> source .bashrc

#### Persist System wide
/etc/environment file
PATH variable -> list of directories to executable files, separated by :
system checks all these locations to find executable file (f.e. java command)
available to all users on system

example: ls command
/usr/bin/ls -> in path variable -> no need to write "/usr/bin/ls" -> "ls" works 

example: write welcome script -> add path to .bashrc (or global path), source .bashrc -> this command is now available from everywhere

### Networking

LAN = Local Area Network; devices connected in one physical location; each device unique IP

IPv4 = 32 Bit value; f.e. 172.16.0.0. -> 0.0.0.0 > 255.255.255.255

Switch: Sits within the LAN; manages connection between devices within LAN
Router: Connect to outside network (WAN = wide are network); connects devices on LAN and WAN; access Internet
Gateway: IP Adress of the router -> Router and network gateway are basically the same thing

How to know whether a device is inside or outside the LAN?;
Devices in the LAN belong to the same IP address range

####Subnet(work)

Subnet: logical subdivision of an IP network
Subnetting: process of dividign a network into two or more networks

Subnet Mask: Sets the ip range

192.168.0.0 255.255.255.0 -> all IP Addresses 192.168.0.x are in range
192.168.0.0 255.255.0.0 -> 192.168.x.x in range

0 means free range
255 fixates the octet (8 bits)

####CIDR (classless inter-domain routing)
shorthand writing

192.168.0.0/16 -> /16 stands for bits that are fixed

Any device needs 3 pieces of data for communication
- IP Address
- Subnet
- Gateway

#### Network Address Translation (NAT)
IP range is chosen by an administrator
each device gets unique ip from that range
-> how to make sure ip addresses dont overlap?

-> (internal) IP addresses of LAN are not visible outside of the network 
-> replaced with IP address of the router
= Key functionality of a router

Advantage
- security of devices in lan
- re-use ip addresses

IPv4 has 4,294,967,296 public addresses available

#### Firewall
Outside device wants to access application running in LAN -> by default not allowed -> Firewall

Firewall = Protection from unauthorized access; rules can be defined
- Which ip address can access my server
- Which ip address is accessible in my network
- with specified port range -> Port Forwarding Configuration

#### Port
Every device has set of ports
-> is like different doors to same building
-> define which ports are accessible

Standard Ports
Web: 80
MySql: 3306
PostgreSQL: 5432

every port is unique on a device

####DNS Domain Name Service
IP addresses are mapped to names (f.e. ip to facebook.com)
DNS = translation of domain names to ip addresses

Hierarchical structure

~ 13 root domains on the world (a-m)
under each root domain there are top level domains (tlds)
6 original TLDs (mil, edu, com, org, net, gov)
country TLDs (at, de, ..)
other TLDs (biz, business, ...)

ICANN
- manages the TLD development and architecture
- authrorizes domain name registrars -> register and assign domain names

scholar.google.com.  = full qualified domain name
subdomain - domain - TLD - root domain

####DNS resolution flow
Every computer has DNS client pre-installed

DNS Client -> Resolver (typically internet service provider) -> if IP Address not in cache -> one of the 13 root servers (available reduntantly all over the world) -> will look at address and send response back to resolver (f.e.: "ask .com server" -> .com server -> returns auth. name server list -> finally have IP address

DNS entries are cached (locally and in resolver)

####Commands
ifconfig -> computer network details
netstat -> active connections
ps aux -> current running applications on ports
nslookup -> get ip address of any domain name; or reverse -> which domain name is attached to specfic ip address
ping Domain/IP -> is address accessible?


___

### SSH (Secure Shell)

- copy file to remote server
- install software on new server

-> secure network protocoll to connect to a computer over the internet
-> also revers to suite of uitlities that implement this protocol

Authenticate with remote server
- username & password (created on remote server)
- or: ssh key pair (more secure): client machine creates ssh key pair (private + public); private key is stored on client machine; public key is shared with remote server; client can unluck the public key with his private key

SSH for services
f.e.: Jenkins
1. create jenkins user on application server
2. create ssh key pair on jenkins server
3. add public ssh key to authorized keys on application server

#### Firewall and Port 22
As learned above: connection must be explicitly allowed by firewall to be possible
SSH happens AFTER the connection!
-> FIRST connection must be allowed, then authentication can be verified
-> on most OS SSH service runs on Port 22 -> in firewall assure access to port 22 is allowed for specific white listed ip addresses

#### Demo DigitalOcean

created a droplet in DigitalOcean (by default all ports are open, can  be changed in networking)

in local terminal: ssh root@IP -> connected with password

#### Connect with SSH KeyPair

On Local machine
ssh-keygen -t rsa -> generate ssh keypair
cat .ssh/id_rsa.pub -> our public key (file name varies depending on ssh key name)

On server
ls .ssh -> we find authorized_keys file
vim .ssh/authorized_keys -> add the public key to the file and save

Connect again using ssh root@IP -> no password needed anymore!
ssh -i .ssh/my_ssh_key root@IP -> we pass the location of the private key

__ 
Add a simple script to server

scp (secure copy)
scp SOURCE TARGET
scp test.sh root@IP:/root -> Securely copy the file test.sh to the remote server to folder /root
scp -i .ssh/id_rsa root@IP:/root -> also specify the private key

### Arch/Manjaro/Linux specific steps to add ssh key

ssh-keygen (might be with arguments such as -t rsa) -> name in next step = file path
eval $(ssh-agent)
ssh-add ~/.ssh/PRIVATEKEY




