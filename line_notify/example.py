import json
from line_notify.aws_sns import subscribe


title = ''
msg = 'Hello World!'

event = '{"Records":[{"EventSource":"aws:sns","EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:xxxx","Sns":{"Type":"Notification","MessageId":"xxxx","TopicArn":"arn:aws:sns:xxxx","Subject":"' + title + '","Message":"' + msg + \
    '","Timestamp":"2022-03-05T22:57:07.775Z","SignatureVersion":"1","Signature":"xxx","SigningCertUrl":"https:/example.com","UnsubscribeUrl":"https:/example.com","MessageAttributes":{"level":{"Type":"String","Value":"alert"}}}}]}'
notices = subscribe(json.loads(event))
