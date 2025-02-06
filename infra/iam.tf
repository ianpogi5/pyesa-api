resource "aws_iam_role" "lambda_role" {
  name = "pyesa_api_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Attach permissions for S3 reading + CloudWatch logging
resource "aws_iam_policy" "lambda_logging_policy" {
  name        = "LambdaLoggingPolicy"
  description = "Allows Lambda to write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.S3_BUCKET}",
          "arn:aws:s3:::${var.S3_BUCKET}/*"
        ]
      }
    ]
  })
}

# Attach policy to IAM role
resource "aws_iam_role_policy_attachment" "lambda_logging_attachment" {
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
  role       = aws_iam_role.lambda_role.name
}