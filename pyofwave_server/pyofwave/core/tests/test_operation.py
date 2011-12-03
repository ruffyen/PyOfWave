import unittest
from lxml.builder import ElementMaker
from pyofwave.core import operation, opdev

E = ElementMaker(namespace="pyofwave.info/test")

class TestOperations(unittest.TestCase):
    def testCreateOperation(self):
        NS = opdev.OperationNS("pyofwave.info/test")

        @NS
        def op(event, arg, tag, text, action):
            self.assertEqual(arg, "test")
            self.assertEqual(tag.tag, "{pyofwave.info/test}tag")
            self.assertEqual(text, "hello")
            self.assertEqual(action, "test")
            return NS.E.response("success", status = "400")

    def testPerformOperation(self):
        res = operation.performOperation(None, 
            E.op("test", E.tag(), "hello", action="test"))
        self.assertEqual(res.text, "success")
        self.assertEqual(res.get("status"), "400")

class TestEvents(unittest.TestCase):
    def testOperationEvents(self):
        res = False
        def callback(*args, **kwargs):
            res = True
        URL = "wave://test@pyofwave.info/test"
        evts = operation.Events("test@pyofwave.info", callback)

        # Create an operation for it's event.
        NS = opdev.OperationNS("pyofwave.info/test")
        @NS
        def op(event, *args, **kwargs): pass

        # Trigger event
        evts.register(URL, "{pyofwave.info/test")
        operation.performOperation(evts, E.op(href=URL))
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
