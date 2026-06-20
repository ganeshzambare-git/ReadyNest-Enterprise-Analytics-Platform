terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "streamlit_sg" {
  name        = "readynest_sg"
  description = "Allow inbound traffic for Streamlit app"

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit Port"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "readynest_app" {
  ami           = "ami-0c7217cdde317cfec" # Example Ubuntu 22.04 AMI
  instance_type = "t3.medium"
  vpc_security_group_ids = [aws_security_group.streamlit_sg.id]

  tags = {
    Name = "ReadyNestInsightEngine"
  }
}
