
resource "aws_default_security_group" "default-sg" {
  vpc_id = var.vpc_id

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
    values = [var.image_name]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}


resource "aws_key_pair" "ssh-key" {
  key_name   = "server-key"
  public_key = file(var.public_key_location)
}

resource "aws_instance" "myapp-server" {
  ami                    = data.aws_ami.latest-amazon-linux-image.id #operating system image
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone      = var.avail_zone

  associate_public_ip_address = true #to be able to access it from the internet (browser, ssh)
  key_name                    = aws_key_pair.ssh-key.key_name

  user_data                   = file("entry-script.sh")
  user_data_replace_on_change = true # -> instance is destroyed and recreated if user_data changes

  tags                        = {
    Name : "${var.env_prefix}-server"
  }
}
