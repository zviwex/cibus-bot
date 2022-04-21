# cibus-bot

## Installation
```python3 -m pip install -r requirements.txt```

## Run
```cp cibus.service /etc/systemd/system/```

```service start cibus.service```

## Pre-requisites
Note that this bot's pre-requisites are:
1. Access to DynamoDB table called `accounts` with these permissions
* dynamodb:PutItem
* dynamodb:GetItem
* dynamodb:Scan
* dynamodb:DeleteItem
2. Access to SecretManager with these permissions:
* secretsmanager:GetSecretValue

You can use the terraform module attached and run the service in EC2 with instance profile attaching the role created in the module


## Open issues
* Please note that since this is a POC, the bot is not totally secured. Take a look at [this issue](https://github.com/zviwex/cibus-bot/issues/3)