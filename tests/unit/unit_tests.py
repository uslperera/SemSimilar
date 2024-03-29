import unittest
import HTMLTestRunner

test_modules = [
    'tests.unit.textprocessor.tokenizer',
    'tests.unit.textprocessor.processor',
    'tests.unit.textprocessor.wsd',
    'tests.unit.model.document',
    'tests.unit.similarity_core.corpus.hal',
    'tests.unit.similarity_core.knowledge.lesk',
    'tests.unit.similarity_core.main'
    ]

suite = unittest.TestSuite()

for t in test_modules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suite_fn = getattr(mod, 'suite')
        suite.addTest(suite_fn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
outfile = open("UnitTestsReport.html", "w")
runner = HTMLTestRunner.HTMLTestRunner(
                stream=outfile,
                title='Test Report',
                description='Unit Tests'
                )

runner.run(suite)