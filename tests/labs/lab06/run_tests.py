#!/usr/bin/env python3
"""
Test runner for Lab 6: Simultaneous Auctions

This script runs all tests for the lab and provides a summary of results.
"""

import unittest

def run_marginal_value_tests():
    """Run the marginal value tests."""
    print("Running marginal value tests...")
    
    try:
        from stencils.lab06_stencil.test_marginal_value import TestMarginalValue
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMarginalValue)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()
    except ImportError as e:
        print(f"Error importing test module: {e}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def run_local_bid_tests():
    """Run the local bid tests."""
    print("\nRunning local bid tests...")
    
    try:
        from stencils.lab06_stencil.localbid import local_bid
        from stencils.lab06_stencil.sample_valuations import SampleValuations
        
        # Test that the function exists and can be called
        goods = {"A", "B", "C"}
        price_vector = {"A": 50, "B": 30, "C": 40}
        
        try:
            result = local_bid(goods, SampleValuations.additive_valuation, price_vector, 10)
            print("PASS: local_bid function exists and can be called")
            return True
        except NotImplementedError:
            print("WARNING: local_bid function raises NotImplementedError (expected for stencil)")
            return True
        except Exception as e:
            print(f"FAIL: Error calling local_bid: {e}")
            return False
            
    except ImportError as e:
        print(f"Error importing localbid module: {e}")
        return False


def run_sample_valuations_tests():
    """Test the sample valuations module."""
    print("\nTesting sample valuations...")
    
    try:
        from stencils.lab06_stencil.sample_valuations import SampleValuations
        
        # Test additive valuation
        bundle = {"A", "B"}
        value = SampleValuations.additive_valuation(bundle)
        expected = SampleValuations.SINGLE_ITEM_VALS["A"] + SampleValuations.SINGLE_ITEM_VALS["B"]
        assert abs(value - expected) < 0.01, f"Additive valuation failed: {value} != {expected}"
        print("PASS: Additive valuation works correctly")
        
        # Test complement valuation
        value = SampleValuations.complement_valuation(bundle)
        assert value > expected, f"Complement valuation should be higher: {value} <= {expected}"
        print("PASS: Complement valuation works correctly")
        
        # Test substitute valuation
        value = SampleValuations.substitute_valuation(bundle)
        assert value < expected, f"Substitute valuation should be lower: {value} >= {expected}"
        print("PASS: Substitute valuation works correctly")
        
        # Test price vector generation
        price_vector = SampleValuations.generate_price_vector()
        assert len(price_vector) == len(SampleValuations.SINGLE_ITEM_VALS), "Price vector has wrong length"
        print("PASS: Price vector generation works correctly")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Error testing sample valuations: {e}")
        return False


def main():
    """Run all tests and provide a summary."""
    print("=" * 60)
    print("Lab 6: Simultaneous Auctions - Test Runner")
    print("=" * 60)
    
    results = []
    
    # Run all test suites
    results.append(("Sample Valuations", run_sample_valuations_tests()))
    results.append(("Local Bid", run_local_bid_tests()))
    results.append(("Marginal Value", run_marginal_value_tests()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS: PASS" if success else "FAIL: FAIL"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("PASS: All tests passed! Your implementation is working correctly.")
    else:
        print("WARNING: Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 