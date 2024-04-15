'''The assertIsNot() method is a function of the unittest module in Python that
allows you to test if two objects are NOT the same. It has the following syntax:

assertIs(first, second, msg=None)

The first and second arguments are the objects to be compared, and the msg argument is an optional message to display in case the test fails. The assertIs() method uses the is operator to check if the first and second objects have the same identity, i.e., they refer to the same object in memory.

For example, suppose we have a class called Person that has a name attribute:'''
import unittest

class Person:
    def __init__(self, name):
        self.name = name

##We can use the assertIs() method to test if two instances of Person are the same
# or not:


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p1 = Person("Alice")
        self.p2 = Person("Bob")
        self.p3 = self.p1

    def test_same_person(self):
        # Test if p1 and p3 are the same object
        self.assertIs(self.p1, self.p3)

    def test_different_person(self):
        # Test if p1 and p2 are different objects
        self.assertIs(self.p1, self.p2)

    def test_none(self):
        # Test if an object is None
        self.assertIs(self.p4, None)

if __name__ == "__main__":
    unittest.main()