#!/usr/bin/env python3
"""
Test cases for marginal value calculation.
Students implement test cases to verify their understanding of marginal values.
"""

import unittest
from marginal_value import calculate_marginal_value


def test_example_case():
    """
    Example test case provided in the writeup.
    """
    # Define goods
    goods = {"camera", "flash"}
    
    # Define valuation function: camera and flash together = 500, either alone = 1
    def valuation_function(bundle):
        if "camera" in bundle and "flash" in bundle:
            return 500
        elif "camera" in bundle or "flash" in bundle:
            return 1
        else:
            return 0
    
    # Define bids and prices
    bids = {"camera": 500, "flash": 500}  # High bids
    prices = {"camera": 200, "flash": 100}  # Other agent bids
    
    # Test marginal value of camera
    mv_camera = calculate_marginal_value(goods, "camera", valuation_function, bids, prices)
    print(f"Marginal value of camera: {mv_camera}")
    
    # Test marginal value of flash
    mv_flash = calculate_marginal_value(goods, "flash", valuation_function, bids, prices)
    print(f"Marginal value of flash: {mv_flash}")


def test_student_case_1():
    """
    TODO: Implement your first test case here.
    
    This should test a simple scenario to verify your understanding of marginal values.
    """
    # TODO: Implement test case 1
    raise NotImplementedError("Implement test case 1")


def test_student_case_2():
    """
    TODO: Implement your second test case here.
    
    This should test a more complex scenario with complements or substitutes.
    """
    # TODO: Implement test case 2
    raise NotImplementedError("Implement test case 2")


def test_student_case_3():
    """
    TODO: Implement your third test case here.
    
    This should test edge cases or boundary conditions.
    """
    # TODO: Implement test case 3
    raise NotImplementedError("Implement test case 3")


class TestMarginalValue(unittest.TestCase):
    """Unit tests for marginal value calculation."""
    
    def test_example_case(self):
        """Test the example case from the writeup."""
        test_example_case()
    
    def test_student_case_1(self):
        """Test student's first test case."""
        test_student_case_1()
    
    def test_student_case_2(self):
        """Test student's second test case."""
        test_student_case_2()
    
    def test_student_case_3(self):
        """Test student's third test case."""
        test_student_case_3()


if __name__ == "__main__":
    print("Running marginal value tests...")
    print("=" * 50)
    
    # Run example test
    print("Example test case:")
    test_example_case()
    print()
    
    # Run student tests
    print("Student test cases:")
    try:
        test_student_case_1()
    except NotImplementedError:
        print("Test case 1: Not implemented yet")
    
    try:
        test_student_case_2()
    except NotImplementedError:
        print("Test case 2: Not implemented yet")
    
    try:
        test_student_case_3()
    except NotImplementedError:
        print("Test case 3: Not implemented yet")
    
    print("\nAll tests completed!")
