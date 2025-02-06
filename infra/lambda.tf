resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "pyesa-api-lambda"  # Change to a unique name
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "pyesa_api_lambda.zip"
  source = "../pyesa_api_lambda.zip"
  etag   = filemd5("../pyesa_api_lambda.zip")
}

resource "aws_lambda_function" "pyesa_api_lambda" {
  function_name    = "pyesa_api_lambda"
  role            = aws_iam_role.lambda_role.arn
  handler        = "lambda.handler"
  runtime        = "python3.13"

  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.lambda_zip.key
  source_code_hash = filebase64sha256("../pyesa_api_lambda.zip")

  memory_size   = 256
  timeout       = 15
  environment {
    variables = {
      REDEPLOY = timestamp()  # 👈 Ensures Terraform detects a new deployment
      S3_AWS_REGION = var.region
      S3_BUCKET = var.S3_BUCKET
      MASS_FILES = var.MASS_FILES
    }
  }

  depends_on = [aws_s3_object.lambda_zip]
}