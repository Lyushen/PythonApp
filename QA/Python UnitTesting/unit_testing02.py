'''The assertIsInstance() method is a built-in assertion method in Python’s unittest module,
which helps in validating object classes during unit testing.
The assertIsInstance() method checks if an object belongs to a specific class
or its subclass and raises an AssertionError if it does not. The syntax of the assertIsInstance() method is:

assertIsInstance(obj, cls, msg=None)

where obj is the object to test, cls is a class or a tuple of classes,
and msg is an optional message to display in case of failure. The assertIsInstance() method uses the isinstance() function internally to perform the check.

For example, suppose we have a module called shape.py that defines two classes:
Shape and Square. The Shape class is the base class of the Square class:'''

#To test if an object is an instance of the Square class
# or its subclass, we can use the assertIsInstance() method in a unittest.TestCase subclass:

import unittest
from shapes import Shape, Square


class TestShape(unittest.TestCase):

    def setUp(self):
        self.square = Square()

    def test_is_instance(self):
        self.assertIsInstance(self.square, Square)

    def test_is_instance_of_parent_class(self):
        self.assertIsInstance(self.square, Shape)

if __name__ == '__main__':
    unittest.main()