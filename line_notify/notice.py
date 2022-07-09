from os import getenv
import re


class Notice:
    def __init__(self, content={}) -> None:
        self.set(**content)

    def set(self, to=None, title=None, text=None):
        self.to = to
        self.title = title
        self.text = text
        return self

    def getMsg(self) -> str:
        msg = self.plainMsg()
        for tag in self.getEmojiTags():
            msg = msg.replace(tag, '$')
        return msg

    def plainMsg(self) -> str:
        title = self.title
        text = self.toText(self.text)
        msg = filter(None, [title, text])
        return "\n".join(msg)

    def toText(self, var) -> str:
        if type(var) == str:
            return var
        return str(var)

    def getTo(self) -> str:
        if self.to:
            return self.to
        return getenv('LINE_TO_DEFAULT')

    def getEmojiTags(self):
        msg = self.plainMsg()
        return re.findall(r'\$\{.+:.+\}', msg)

    def getEmojis(self):
        tags = self.getEmojiTags()
        msg = self.plainMsg()
        msg = msg.replace('@', '%')
        for tag in self.getEmojiTags():
            msg = msg.replace(tag, '@')
        indices = [i for i, x in enumerate(msg) if x == '@']
        emojis = [
        ]
        for tag in tags:
            rs = tag.lstrip("${").rstrip("}").split(":")
            emojis.append({
                "index": indices.pop(0),
                "productId": rs[0],
                "emojiId": rs[1],
            }
            )

        return emojis

    def is_broadcast(self) -> bool:
        return self.getTo() == "broadcast"


if __name__ == '__main__':
    import unittest

    class NoticeTest(unittest.TestCase):
        def setUp(self):
            self.s = Notice()

        def testDict(self):
            self.s.set(**{"to": "a123"})
            self.assertEqual("a123", self.s.to)

        def testText(self):
            self.assertEqual("abc", self.s.toText("abc"))
            self.assertEqual("['a']", self.s.toText(["a"]))
            self.assertEqual("{'b': 1}", self.s.toText({"b": 1}))

        def testEmptyTitle(self):
            self.s.set(**{"text": "a123"})
            self.assertEqual("a123", self.s.getMsg())
            self.s.set(**{"text": "a123", "title": ""})
            self.assertEqual("a123", self.s.getMsg())
            self.assertEqual(0, len(self.s.getEmojis()))

        def test_compileEmojis(self):
            self.s.text = '${5ac1bfd5040ab15980c9b435:001}aaa'
            self.assertEqual("$aaa", self.s.getMsg())
            e = {
                "index": 0,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiId": "001"
            }
            self.assertEqual(e, self.s.getEmojis()[0])
            self.assertEqual(1, len(self.s.getEmojis()))
            self.s.text = 'あいう$えお${5ac1bfd5040ab15980c9b435:002}\na${5ac1bfd5040ab15980c9b435:001}aa'
            self.assertEqual("あいう$えお$\na$aa", self.s.getMsg())
            e = {
                "index": 6,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiId": "002"
            }
            self.assertEqual(e, self.s.getEmojis()[0])
            e = {
                "index": 9,
                "productId": "5ac1bfd5040ab15980c9b435",
                "emojiId": "001"
            }
            self.assertEqual(e, self.s.getEmojis()[1])
            self.assertEqual(2, len(self.s.getEmojis()))

        def test_(self):
            self.s.set(**{"to": "broadcast"})
            self.assertTrue(self.s.is_broadcast())
            self.s.set(**{"to": "aaaaaaaa"})
            self.assertFalse(self.s.is_broadcast())
            self.s.set(**{"to": None})
            self.assertFalse(self.s.is_broadcast())

    unittest.main()
