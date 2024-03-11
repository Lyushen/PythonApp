import doctest

def calculate_area(length:int, width:int) -> int:
    """Calculate the area of a rectangle.
    Args:
        length (int): The length of the rectangle.
        width (int): The width of the rectangle.
    Returns:
        int: The area of the rectangle.
    Examples:
        >>> calculate_area(5, 5)
            25
        >>> calculate_area(6, 7)
            42
    """
    return length * width

if __name__ == "__main__":
    doctest.testmod()