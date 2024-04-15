#http: // docs.python.org / library / unittest.html
#demonstrates assertEqual, assertRaise
import unittest

# add, subtract, multiply and divide methods to test
def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        raise ZeroDivisionError
    return x / y

def modulo(x, y):
    if y == 0:
        raise ZeroDivisionError
    return x % y


# create a sublcass of unittest.TestCase
class TestArithmetic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(1, -1), 2)
        self.assertEqual(subtract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(0, 0), 0)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(-4, 2), -2)
        self.assertRaises(ZeroDivisionError, divide, 1, 0)

    def test_modulo(self):
        self.assertEqual(modulo(16, 3), 1)
        self.assertEqual(modulo(-4, 2), 0)
        self.assertRaises(ZeroDivisionError, modulo, 1, 0)

if __name__ == '__main__':
    unittest.main()
