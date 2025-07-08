#!/usr/bin/env python3
"""
Test runner for Lab 7: Simultaneous Auctions (Part 2)

This script runs all tests for the lab and provides a summary of results.
"""

import unittest

def run_histogram_tests():
    """Run the histogram tests."""
    print("Running histogram tests...")
    
    try:
        from stencils.lab07_stencil.single_good_histogram import SingleGoodHistogram
        from stencils.lab07_stencil.independent_histogram import IndependentHistogram
        
        # Test that classes can be instantiated
        hist = SingleGoodHistogram(bucket_size=5, bid_upper_bound=100)
        print("PASS: SingleGoodHistogram can be instantiated")
        
        ind_hist = IndependentHistogram(["A", "B"], [5, 5], [100, 100])
        print("PASS: IndependentHistogram can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Error testing histograms: {e}")
        return False


def run_marginal_value_tests():
    """Run the marginal value tests."""
    print("\nRunning marginal value tests...")
    
    try:
        from stencils.lab07_stencil.marginal_value import calculate_marginal_value, calculate_expected_marginal_value
        
        # Test that functions exist
        goods = {"A", "B"}
        bids = {"A": 10, "B": 15}
        prices = {"A": 8, "B": 12}
        
        def valuation(bundle):
            return sum(10 for item in bundle)
        
        try:
            mv = calculate_marginal_value(goods, "A", valuation, bids, prices)
            print("PASS: calculate_marginal_value function works")
        except NotImplementedError:
            print("WARNING: calculate_marginal_value raises NotImplementedError (expected for stencil)")
        
        try:
            from stencils.lab07_stencil.independent_histogram import IndependentHistogram
            price_dist = IndependentHistogram(goods, [5, 5], [100, 100])
            expected_mv = calculate_expected_marginal_value(goods, "A", valuation, bids, price_dist)
            print("PASS: calculate_expected_marginal_value function works")
        except NotImplementedError:
            print("WARNING: calculate_expected_marginal_value raises NotImplementedError (expected for stencil)")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Error testing marginal value: {e}")
        return False


def run_local_bid_tests():
    """Run the local bid tests."""
    print("\nRunning local bid tests...")
    
    try:
        from stencils.lab07_stencil.localbid import expected_local_bid
        from stencils.lab07_stencil.independent_histogram import IndependentHistogram
        
        def valuation(bundle):
            return sum(10 for item in bundle)
        
        goods = ["A", "B", "C"]
        price_dist = IndependentHistogram(goods, [5, 5, 5], [100, 100, 100])
        
        try:
            result = expected_local_bid(goods, valuation, price_dist, num_iterations=10, num_samples=50)
            print("PASS: expected_local_bid function works")
            return True
        except NotImplementedError:
            print("WARNING: expected_local_bid raises NotImplementedError (expected for stencil)")
            return True
            
    except Exception as e:
        print(f"FAIL: Error testing local bid: {e}")
        return False


def run_agent_tests():
    """Run the agent tests."""
    print("\nRunning agent tests...")
    
    try:
        from stencils.lab07_stencil.scpp_agent import SCPPAgent
        from stencils.lab07_stencil.competition_agent import CompetitionAgent
        
        # Test that agents can be instantiated
        agent1 = SCPPAgent("TestSCPP")
        print("PASS: SCPPAgent can be instantiated")
        
        agent2 = CompetitionAgent("TestComp")
        print("PASS: CompetitionAgent can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Error testing agents: {e}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("\nRunning integration tests...")
    
    try:
        # Test that all components can be imported together
        from stencils.lab07_stencil.single_good_histogram import SingleGoodHistogram
        from stencils.lab07_stencil.independent_histogram import IndependentHistogram
        from stencils.lab07_stencil.marginal_value import calculate_marginal_value, calculate_expected_marginal_value
        from stencils.lab07_stencil.localbid import expected_local_bid
        from stencils.lab07_stencil.scpp_agent import SCPPAgent
        from stencils.lab07_stencil.competition_agent import CompetitionAgent
        
        print("PASS: All components can be imported together")
        
        # Test basic functionality
        goods = {"A", "B"}
        hist = SingleGoodHistogram(bucket_size=5, bid_upper_bound=100)
        ind_hist = IndependentHistogram(goods, [5, 5], [100, 100])
        
        print("PASS: Basic histogram functionality works")
        
        return True
        
    except Exception as e:
        print(f"FAIL: Error in integration tests: {e}")
        return False


def main():
    """Run all tests and provide a summary."""
    print("=" * 60)
    print("Lab 7: Simultaneous Auctions (Part 2) - Test Runner")
    print("=" * 60)
    
    results = []
    
    # Run all test suites
    results.append(("Histograms", run_histogram_tests()))
    results.append(("Marginal Value", run_marginal_value_tests()))
    results.append(("Local Bid", run_local_bid_tests()))
    results.append(("Agents", run_agent_tests()))
    results.append(("Integration", run_integration_tests()))
    
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
        print("PASS: All tests passed! Your stencils are ready for implementation.")
    else:
        print("WARNING: Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 