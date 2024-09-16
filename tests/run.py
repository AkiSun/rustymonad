import unittest


test_cases = unittest.defaultTestLoader.discover('.')
suite = unittest.TestSuite(test_cases)

unittest.TextTestRunner(verbosity=2).run(suite)
