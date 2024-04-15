'''The assertIs() method has a counterpart called assertIsNot(),
which tests if two objects are not the same. It has the same syntax as assertIs(),
but it uses the is not operator instead of the is operator. For example:'''


import unittest

class Person:
    def __init__(self, name):
        self.name = name

##We can use the assertIsNot() method to test if two instances of Person are NOT the same



class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p1 = Person("Alice")
        self.p2 = Person("Bob")
        self.p3 = self.p1

    def test_same_person(self):
        # Test if p1 and p3 are NOT the same object
        self.assertIsNot(self.p1, self.p3)

    def test_different_person(self):
        # Test if p1 and p2 are NOT different objects
        self.assertIsNot(self.p1, self.p2)

    def test_not_none(self):
        # Test if an object is not None
        self.assertIsNot(self.p1, None)

if __name__ == "__main__":
    unittest.main()