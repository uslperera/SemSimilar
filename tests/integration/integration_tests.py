import unittest
from tests.unit import HTMLTestRunner

test_modules = [
    'tests.integration.model.document_worker',
    'tests.integration.model.document',
    'tests.integration.similarity_core.corpus.hal',
    'tests.integration.similarity_core.knowledge.lesk',
    'tests.integration.similarity_core.main'
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

outfile = open("IntegrationTestsReport.html", "w")
runner = HTMLTestRunner.HTMLTestRunner(
                stream=outfile,
                title='Test Report',
                description='Integration Tests'
                )

runner.run(suite)