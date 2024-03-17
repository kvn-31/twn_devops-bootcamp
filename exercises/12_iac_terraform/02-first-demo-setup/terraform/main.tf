provider "aws" {
  region     = "eu-central-1"
}

variable "cidr_blocks" {
  description = "cidr blocks"
  type = list(object({
    cidr_block = string
    name = string
  }))
}

variable environment {
  description = "env"
}

variable avail_zone {
}

resource "aws_vpc" "development-vpc" {
  cidr_block = var.cidr_blocks[0].cidr_block
  tags = {
    Name: var.cidr_blocks[0].name #Name key is reserved for name of the resource
  }
}

resource "aws_subnet" "dev-subnet-1" {
  vpc_id            = aws_vpc.development-vpc.id #reference resource defined in same context
  cidr_block        = var.cidr_blocks[1].cidr_block
  availability_zone = var.avail_zone
  tags = {
    Name: var.cidr_blocks[1].name #Name key is reserved for name of the resource
  }
}

#data source to filter vpc with custom name "existing_vpc"
data "aws_vpc" "existing_vpc" {
  #arguments to filter vpc
  default = true
}

resource "aws_subnet" "dev-subnet-2" {
  vpc_id            = data.aws_vpc.existing_vpc.id #reference data source defined in same context
  cidr_block        = "172.31.48.0/20"
  availability_zone = "eu-central-1a"
  tags = {
    Name: "subnet-default" #Name key is reserved for name of the resource
  }
}

output "dev-vpc-id" {
  value = aws_vpc.development-vpc.id
}

output "dev-subnet-id" {
  value = aws_subnet.dev-subnet-1.id
}
