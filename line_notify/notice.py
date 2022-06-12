from os import getenv


class Notice:
    def __init__(self, content={}) -> None:
        self.set(**content)

    def set(self, to=None, title=None, text=None):
        self.to = to
        self.title = title
        self.text = text
        return self

    def getMsg(self) -> str:
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
            self.s.set(**{"text": "a123", "title":""})
            self.assertEqual("a123", self.s.getMsg())

    unittest.main()
