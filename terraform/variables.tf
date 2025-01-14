variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for RDS"
  type        = string
}

variable "private_subnets" {
  description = "The private subnets for ECS tasks"
  type        = map(list(string))
}

variable "security_groups" {
  description = "The security groups to assign to resources"
  type        = map(list(string))
}

variable "domain_name" {
  description = "Domain name for DNS records"
  type        = string
}

variable "route53_zone_id" {
  description = "Route 53 Zone ID"
  type        = string
}

variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}
