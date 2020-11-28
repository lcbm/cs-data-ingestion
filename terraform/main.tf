terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.18.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Create a VPC to launch our instances into
resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "cs_data_ingestion"
  }
}


# Create a subnet to launch our instances into
resource "aws_subnet" "default" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-west-1a"

  depends_on = [aws_vpc.default]

  tags = {
    Name = "cs_data_ingestion"
  }
}

# Create an internet gateway to give our subnet access to the outside world
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id

  depends_on = [aws_vpc.default]

  tags = {
    Name = "cs_data_ingestion"
  }
}

# Grant the VPC internet access on its main route table
resource "aws_route_table" "internet_access" {
  vpc_id = aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

  tags = {
    Name = "cs_data_ingestion"
  }
}

resource "aws_route_table_association" "table_association" {
  subnet_id      = aws_subnet.default.id
  route_table_id = aws_route_table.internet_access.id
}

# Our default security group to access
# the instances over SSH and HTTP
resource "aws_security_group" "default" {
  vpc_id = aws_vpc.default.id

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from the VPC
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  # Frontend
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cs_data_ingestion"
  }
}

resource "aws_key_pair" "auth" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)

  tags = {
    Name = "cs_data_ingestion"
  }
}

resource "aws_instance" "web" {
  ami           = var.aws_ami
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.default.id]
  key_name               = aws_key_pair.auth.key_name

  subnet_id = aws_subnet.default.id

  root_block_device {
    volume_type = "gp2"
    volume_size = 30
  }

  connection {
    type = "ssh"
    user = "ubuntu"
    host = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo snap install docker",
      "sudo snap services docker",
      "git clone https://github.com/lcbm/cs-data-ingestion.git",
      "cd cs-data-ingestion",
      "git checkout -b dev origin/dev",
      "sudo docker build . -f frontend/Dockerfile-dev -t cs-data-ingestion:frontend",
      "sudo docker run -d --name frontend -p 5000:5000 cs-data-ingestion:frontend"
    ]
  }

  tags = {
    Name = "cs_data_ingestion"
  }
}
