resource "aws_dynamodb_table" "accounts" {
  name         = "accounts"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userid"
  attribute {
    name = "userid"
    type = "S"
  }
}

resource "aws_iam_role" "bot-role" {
  name = "bot-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = [
            "ec2.amazonaws.com"
            ],
        }
        Effect = "Allow"
        Sid = "ec2"
      }
    ]
  })


  inline_policy {
    name = "bot_inline_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [

        {
          Action: [
            "dynamodb:PutItem",
            "dynamodb:GetItem",
            "dynamodb:Scan",
            "dynamodb:DeleteItem",
          ]
          Effect   = "Allow"
          Resource = aws_dynamodb_table.accounts.arn
        },
        {
          Action   = [
            "secretsmanager:GetSecretValue",
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}
