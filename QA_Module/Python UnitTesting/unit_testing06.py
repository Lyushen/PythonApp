
# The assertIn method of the unittest module is used to check if an item
# is present in a container, such as a list, a tuple, a set, or a dictionary.
# For example, if we want to test if the number 3 is in a list called numbers,
# we can write:

import unittest


class TestNumbers(unittest.TestCase):

    def setUp(self):
        self.numbers = [1, 2, 3, 4, 5]

    def test_3_in_numbers(self):
        self.assertIn(3, self.numbers)

        # The assertIn method will pass the test if the first argument
        # is in the second argument, and fail the test otherwise.
        # It is equivalent to using the in operator in Python, such as:
        #assert 3 in numbers

        # The assertIn method can also take an optional third argument,
        # which is a message that will be displayed if the test fails.
        # For example:

        self.assertIn(3, self.numbers, "3 is not in the list")

        # The assertIn method has a counterpart called assertNotIn,
        # which checks if an item is not present in a container.
        # The assertNotIn method will pass the test if the first argument
        # is not in the second argument, and fail the test otherwise.
        # For example:

        self.assertNotIn(6, self.numbers)

        # The assertNotIn method will pass the test if the first argument
        # is not in the second argument, and fail the test otherwise.
if __name__ == '__main__':
    unittest.main()