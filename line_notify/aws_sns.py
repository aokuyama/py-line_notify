from line_notify.notice import Notice
from line_notify.bot import LineBot


def subscribe(event):
    bot = LineBot()
    notices = by_event(event)
    if not notices:
        return False
    for n in notices:
        bot.send(n)
    return True


def by_event(event):
    if 'Records' not in event:
        return False
    notices = []
    for record in event['Records']:
        notices.append(by_record(record))
    return notices


def by_record(record):
    sns = record['Sns']
    con = {'title': sns['Subject'], 'text': sns['Message']}
    if 'MessageAttributes' in sns:
        attr = sns['MessageAttributes']
        if 'to' in attr:
            con['to'] = attr['to']['Value']
        if 'reply_token' in attr:
            con['reply_token'] = attr['reply_token']['Value']
    return Notice(con)


if __name__ == '__main__':
    import unittest
    import json

    class NoticeTest(unittest.TestCase):
        def setUp(self):
            pass

        def test_init_by_records(self):
            event = '{"Records":[{"EventSource":"aws:sns","EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:xxxx","Sns":{"Type":"Notification","MessageId":"xxxx","TopicArn":"arn:aws:sns:xxxx","Subject":"subjectbysns","Message":"msgbysns","Timestamp":"2022-03-05T22:57:07.775Z","SignatureVersion":"1","Signature":"xxx","SigningCertUrl":"https:/example.com","UnsubscribeUrl":"https:/example.com","MessageAttributes":{"reply_token":{"Type":"String","Value":"tokenaaa"},"level":{"Type":"String","Value":"alert"}}}},{"EventSource":"aws:sns","EventVersion":"1.0","EventSubscriptionArn":"arn:aws:sns:xxxx","Sns":{"Type":"Notification","MessageId":"xxxx","TopicArn":"arn:aws:sns:xxxx","Subject":"subjectbysns2","Message":"msgbysns2","Timestamp":"2022-03-05T22:57:07.775Z","SignatureVersion":"1","Signature":"xxx","SigningCertUrl":"https:/example.com","UnsubscribeUrl":"https:/example.com","MessageAttributes":{"to":{"Type":"String","Value":"abcdefg"}}}}]}'
            notices = by_event(json.loads(event))
            self.assertEqual(2, len(notices))
            self.assertEqual('subjectbysns', notices[0].title)
            self.assertEqual('msgbysns', notices[0].text)
            self.assertIsNone(notices[0].to)
            self.assertEqual('tokenaaa', notices[0].reply_token)
            self.assertEqual('subjectbysns2', notices[1].title)
            self.assertEqual('msgbysns2', notices[1].text)
            self.assertEqual('abcdefg', notices[1].to)
            self.assertIsNone(notices[1].reply_token)
    unittest.main()
