import unittest

# Assuming the Calculate_area function is defined somewhere
def Calculate_area(length, width):
    if length < 0 or width < 0:
        raise ValueError("Length and width must be non-negative")
    return length * width

class TestCalculateArea(unittest.TestCase):
    def test_area_calculation(self):
        try:
            result = Calculate_area(5, 2)
            expected = 9
            self.assertEqual(result, expected)
        except AssertionError as e:
            self.fail(f"Test failed with: {str(e)}")

    def test_negative_values(self):
        try:
            Calculate_area(-5, 2)
            self.fail("Expected ValueError for negative dimensions")
        except ValueError as e:
            pass  # Test passes as the exception is expected
        except Exception as e:
            self.fail(f"Unexpected exception thrown: {str(e)}")

if __name__ == '__main__':
    unittest.main()