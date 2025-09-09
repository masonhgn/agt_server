"""
Test cases for marginal value calculation.
Students implement test cases to verify their understanding of marginal values.
"""

import unittest
from marginal_value import calculate_marginal_value

class TestMarginalValue(unittest.TestCase):
    """Unit tests for marginal value calculation."""
    
    def test_example_case_one(self):
        goods = {"A", "B"}
        bids = {"A": 95, "B": 90}
        prices = {"A": 80, "B": 80}

        def valuation(bundle):
            if "A" in bundle and "B" in bundle:
                return 100
            elif "A" in bundle:
                return 90
            elif "B" in bundle:
                return 70
            return 0

        mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)

        expected_mv_a = 30

        self.assertAlmostEqual(mv_a, expected_mv_a, places=3, msg=f"Incorrect marginal value for A: expected {expected_mv_a}, got {mv_a}")


    def test_example_case_no_goods_won(self):
        goods = {"A", "B"}
        bids = {"A": 50, "B": 50}
        prices = {"A": 100, "B": 100}

        def valuation(bundle): 
            return len(bundle) * 10 

        mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)
        mv_b = calculate_marginal_value(goods, "B", valuation, bids, prices)

        self.assertEqual(mv_a, 10, "Incorrect marginal value for A")
        self.assertEqual(mv_b, 10, "Incorrect marginal value for B")

    def test_student_case_1(self):
        """
        TODO: Implement your first test case here.
        
        This should test a simple scenario to verify your understanding of marginal values.
        """
        # TODO: Implement test case 1
        raise NotImplementedError("Implement test case 1")


    def test_student_case_2(self):
        """
        TODO: Implement your second test case here.
        
        This should test a more complex scenario with complements or substitutes.
        """
        # TODO: Implement test case 2
        raise NotImplementedError("Implement test case 2")


    def test_student_case_3(self):
        """
        TODO: Implement your third test case here.
        
        This should test edge cases or boundary conditions.
        """
        # TODO: Implement test case 3
        raise NotImplementedError("Implement test case 3")


if __name__ == "__main__":
    unittest.main()