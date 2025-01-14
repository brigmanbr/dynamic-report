environment     = "prod"
vpc_id          = "vpc-0df119ea06f9fbe79"
private_subnets = { prod = ["subnet-008219a1fd0327de9", "subnet-0e17c230b027ed06e", "subnet-0c0a8da32f8c2bc51"] }
security_groups = { prod = ["sg-037a0bc67ade56c54", "sg-03ed0e34669db331c", "sg-0a4da5958cfa160de"] }
route53_zone_id = "Z02046953BKXANG0AAXJI" # Replace with your Route53 hosted zone ID
domain_name     = "wudtr.com"
