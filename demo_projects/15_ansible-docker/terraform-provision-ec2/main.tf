provider "aws" {
  region = "eu-central-1"
}

variable vpc_cidr_block {}
variable "subnet_cidr_block" {}
variable avail_zone {}
variable env_prefix {}
variable my_ip {}
variable instance_type {}
variable public_key_location {}

resource "aws_vpc" "myapp-vpc" {
  cidr_block = var.vpc_cidr_block
  tags       = {
    Name : "${var.env_prefix}-vpc"
  }
}

resource "aws_subnet" "myapp-subnet-1" {
  #is implicitly associated with the main route table
  vpc_id            = aws_vpc.myapp-vpc.id
  cidr_block        = var.subnet_cidr_block
  availability_zone = var.avail_zone
  tags              = {
    Name : "${var.env_prefix}-subnet-1"
  }
}

# commented, now we use the default route table
/*resource "aws_route_table" "myapp-route-table" {
  vpc_id = aws_vpc.myapp-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.myapp-igw.id
  }
  tags = {
    Name : "${var.env_prefix}-rtb"
  }
}*/
#resource "aws_route_table_association" "a-rtb-subnet" {
#  subnet_id      = aws_subnet.myapp-subnet-1.id
#  route_table_id = aws_route_table.myapp-route-table.id
#}

resource "aws_internet_gateway" "myapp-igw" {
  vpc_id = aws_vpc.myapp-vpc.id
  tags   = {
    Name : "${var.env_prefix}-igw"
  }
}

resource "aws_default_route_table" "main-rtb" {
  default_route_table_id = aws_vpc.myapp-vpc.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.myapp-igw.id
  }
  tags = {
    Name : "${var.env_prefix}-main-rtb"
  }
}

resource "aws_default_security_group" "default-sg" {
  vpc_id = aws_vpc.myapp-vpc.id

  # ingress for incoming traffic like ssh, access from browser
  ingress {
    from_port   = 22 #it is a range -> we only allow 22 for ssh
    to_port     = 22
    protocol    = "TCP"
    cidr_blocks = [var.my_ip] #who is allowed to access
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"] #everyone is allowed to access
  }

  # egress for outgoing traffic, for installation, fetch images, etc
  egress {
    from_port       = 0 #any port
    to_port         = 0
    protocol        = "-1" #any protocol
    cidr_blocks     = ["0.0.0.0/0"] #any ip
    prefix_list_ids = []
  }

  tags = {
    Name : "${var.env_prefix}-default-sg"
  }
}

# dynamically get the latest amazon linux image
data "aws_ami" "latest-amazon-linux-image" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-*-x86_64-gp2"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

output "aws_ami_id" {
  value = data.aws_ami.latest-amazon-linux-image.id
}

output "ec2_public_ip" {
  value = aws_instance.myapp-server.public_ip
}

resource "aws_key_pair" "ssh-key" {
  key_name   = "server-key"
  public_key = file(var.public_key_location)
}

resource "aws_instance" "myapp-server" {
  ami                    = data.aws_ami.latest-amazon-linux-image.id #operating system image
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.myapp-subnet-1.id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone      = var.avail_zone

  associate_public_ip_address = true #to be able to access it from the internet (browser, ssh)
  key_name                    = aws_key_pair.ssh-key.key_name

  tags                        = {
    Name : "${var.env_prefix}-server"
  }
}

