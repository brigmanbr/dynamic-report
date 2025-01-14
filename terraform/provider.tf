terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.67.0"
    }

  }

  backend "s3" {
    bucket         = "terraform-remote-state-dont-delete"
    key            = "dynamic-report/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "fa604bdb-8274-4a42-91a1-7083bb6043f5"
    dynamodb_table = "tf-remote-state-lock"
  }
}

provider "aws" {
  region  = "us-east-1"
}
