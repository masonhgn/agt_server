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
    
    Algorithm 2: LocalBid with Price Sampling
    INPUTS: Set of goods G, valuation function v, price distribution P
    HYPERPARAMETERS: NUM_ITERATIONS, NUM_SAMPLES
    OUTPUT: A bid vector of average marginal values
    
    Initialize bid vector b_old with a bid for each good in G
    for NUM_ITERATIONS or until convergence do
        b_new ← b_old.copy()
        for each gk ∈ G do
            MV ← CalcExpectedMarginalValue(G, gk, v, b_old, P)
            b_new,k ← MV
        end for
        b_old ← b_new
    end for
    return b_old
    """
    # Initialize bid vector with zeros
    b_old = {good: 0.0 for good in goods}
    
    for iteration in range(num_iterations):
        b_new = b_old.copy()
        
        for good in goods:
            # Calculate expected marginal value for this good
            expected_mv = calculate_expected_marginal_value(
                goods, good, valuation_function, b_old, price_distribution, num_samples
            )
            b_new[good] = expected_mv
        
        # Check for convergence (simple approach: if no significant change)
        max_change = max(abs(b_new[good] - b_old[good]) for good in goods)
        if max_change < 0.01:  # Convergence threshold
            break
            
        b_old = b_new
    
    return b_new

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
