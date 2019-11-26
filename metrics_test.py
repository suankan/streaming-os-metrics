'''
This is a module with unit test for Metrics class
'''

import unittest
from metrics import Metrics

class TestMetrics(unittest.TestCase):
    '''
    This are the unit tests for class Metrics.

    There are quite a few different get_* methods inside the Metrics class.
    And going forward there might be more added in future.

    Right now each get_* method is just a wrapper around corresponding psutil library function.
    The main idea of Metrics class is to "normalise" and "beautify" the metrics output.
    It should be clear from the first glance which metric does each value correspond to.

    To achieve that we transform the default output of psutil library functions to be a dictionary.
    In that way we always can guarantee that each value will described by some key-name.

    At the same time we don't know exactly what all get_* methods are returning in different OS.
    And we don't really want to test that.
    But at least we want to make sure that all functions starting with get_* return dictionary.
    That will ensure that all attributes of Metrics class will be JSON serialised in a clear way.
    '''

    def bootstrap_test(self):
        '''
        Initialise Metrics object and take list of all methods that start with "get_"
        '''
        self.metrics = Metrics()
        # Introspect metrics object and get all callable methods which start with "get_"
        self.get_methods = [f for f in dir(self.metrics) if callable(getattr(self.metrics, f)) and f.startswith('get_')]

    def test_get_methods_return_dict(self):
        '''
        Test that all get_ methods in object of class Metrics return dict
        '''
        self.bootstrap_test()

        for func_name in self.get_methods:
            print(f"Testing method {func_name}")
            func = getattr(self.metrics, func_name)
            func_result = func()
            # print(f"Class method {func_name} result {func_result}")

            actual_result = type(func_result)

            self.assertEqual(actual_result, dict, f"Class method {func_name} must return dictionary.")

if __name__ == '__main__':
    unittest.main()