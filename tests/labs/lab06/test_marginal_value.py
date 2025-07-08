import unittest
from stencils.lab06_stencil.marginal_value import calculate_marginal_value

class TestMarginalValue(unittest.TestCase):

    def test_example_case(self):
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


    def test_no_goods_won(self):
        goods = {"A", "B"}
        bids = {"A": 50, "B": 50}
        prices = {"A": 100, "B": 100}

        def valuation(bundle): 
            return len(bundle) * 10 

        mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)
        mv_b = calculate_marginal_value(goods, "B", valuation, bids, prices)

        self.assertEqual(mv_a, 10, "Incorrect marginal value for A")
        self.assertEqual(mv_b, 10, "Incorrect marginal value for B")

    #TODO: Fill in test cases
    # def test_student_case_1(self):
    #     """Student test case 1"""
    #     
    #     goods = ???
    #     bids = ???
    #     prices = ???

    #     def student_valuation(bundle):
    #         ???

    #     ??? = calculate_marginal_value(goods, ???, student_valuation, bids, prices)

    #     self.assertEqual(???, 0, "TODO: Replace with correct expected value")

    # def test_student_case_2(self):
    #     """Student test case 2"""
    #     
    #     goods = ???
    #     bids = ???
    #     prices = ???

    #     def student_valuation(bundle):
    #         ???

    #     ??? = calculate_marginal_value(goods, ???, student_valuation, bids, prices)

    #     self.assertEqual(???, 0, "TODO: Replace with correct expected value")
    
    # def test_student_case_3(self):
    #     """Student test case 3"""
    #     
    #     goods = ???
    #     bids = ???
    #     prices = ???

    #     def student_valuation(bundle):
    #         ???

    #     ??? = calculate_marginal_value(goods, ???, student_valuation, bids, prices)

    #     self.assertEqual(???, 0, "TODO: Replace with correct expected value")


if __name__ == "__main__":
    unittest.main() 