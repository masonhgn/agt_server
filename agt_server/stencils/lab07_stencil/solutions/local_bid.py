"""
Solution for local bid implementation.
"""

import sys
import os

# Add parent directory to path to import from solution files
sys.path.insert(0, os.path.dirname(__file__))

from marginal_values import calculate_expected_marginal_value
from independent_histogram import IndependentHistogram


def expected_local_bid(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
    """
    Iteratively computes a bid vector by updating bids to be the expected marginal value for each good.
    
    """
    bid_vector = {good: 0.0 for good in goods}
    for _ in range(num_iterations):
        new_bid_vector = {}
        #print(bid_vector)
        for good in goods:
            mv = calculate_expected_marginal_value(goods, good, valuation_function, bid_vector, price_distribution, num_samples)
            new_bid_vector[good] = mv
        bid_vector = new_bid_vector
    return bid_vector

if __name__ == "__main__":
    # Test with a simple additive valuation function
    # This mimics how the old server generated valuations
    def test_valuation(bundle):
        """Simple additive valuation for testing."""
        base_values = {"a": 20, "b": 25, "c": 30}
        return sum(base_values.get(item, 0) for item in bundle)
    
    # Create a simple price distribution for testing
    test_histogram = IndependentHistogram(["a", "b", "c"], [5, 5, 5], [100, 100, 100])
    
    # Add some sample data to the histogram
    for _ in range(10):
        test_histogram.add_record({"a": 15, "b": 20, "c": 25})
    
    print("Testing expected_local_bid with sample data...")
    result = expected_local_bid(
        goods=["a", "b", "c"],
        valuation_function=test_valuation,
        price_distribution=test_histogram,
        num_iterations=10,
        num_samples=50
    )
    print("Result:", result)
