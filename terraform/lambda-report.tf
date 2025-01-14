# IAM Role for Lambda
resource "aws_iam_role" "lambda_report_role" {
  name = "lambda_report_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM Policy Attachment for Lambda Basic Execution
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_report_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM Policy for Lambda VPC Access
resource "aws_iam_policy" "lambda_vpc_permissions" {
  name        = "${var.environment}-lambda-vpc-permissions"
  description = "Permissions for Lambda to access VPC resources"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
        ],
        Resource = "*"
      }
    ]
  })
}

# IAM Policy Attachment for Lambda VPC Access
resource "aws_iam_role_policy_attachment" "lambda_vpc_permissions_attachment" {
  role       = aws_iam_role.lambda_report_role.name
  policy_arn = aws_iam_policy.lambda_vpc_permissions.arn
}

# Lambda Function ZIP File
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../src"  # Adjusted to point to the src directory relative to the root
  output_path = "../src/output/lambda_report_function.zip"  # Specify output path
}


# Security Group for Lambda
resource "aws_security_group" "lambda_sg" {
  name        = "${var.environment}-lambda-sg"
  description = "Security group for Lambda function"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # All traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Lambda Function
resource "aws_lambda_function" "lambda_report_function" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "example_lambda_report_function"
  role             = aws_iam_role.lambda_report_role.arn
  handler          = "lambda_report_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.9"

  vpc_config {
    subnet_ids         = var.private_subnets[var.environment]
    security_group_ids = var.security_groups[var.environment]
  }

}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_report_function.function_name}"
  retention_in_days = 14
}
