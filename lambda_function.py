from line_notify.aws_sns import subscribe

def lambda_handler(event, context):
    subscribe(event)
