"""
Solution for local bid implementation.
"""

import sys
import os

# Add parent directory to path to import from solution files
sys.path.insert(0, os.path.dirname(__file__))

from marginal_values import calculate_expected_marginal_value
from independent_histogram import IndependentHistogram


def local_bid(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
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
    bids = {good: 0.0 for good in goods}
    
    for iteration in range(num_iterations):
        # Create a copy of current bids
        new_bids = bids.copy()
        
        # Update each good's bid to its expected marginal value
        for good in goods:
            expected_mv = calculate_expected_marginal_value(
                goods, good, valuation_function, bids, price_distribution, num_samples
            )
            new_bids[good] = expected_mv
        
        # Update bids for next iteration
        bids = new_bids
        
        # Optional: Check for convergence
        if iteration > 0:
            max_change = max(abs(bids[good] - new_bids[good]) for good in goods)
            if max_change < 0.01:  # Small threshold for convergence
                break
    
    return bids

if __name__ == "__main__":
    def valuation(bundle): 
        if len(bundle) == 1: 
            return 10 
        elif len(bundle) == 2:
            return 80 
        elif len(bundle) == 3: 
            return 50 
        else: 
            return 0
    
    print(local_bid(
        goods=["a", "b", "c"],
        valuation_function=valuation,
        price_distribution=IndependentHistogram(["a", "b", "c"], 
                                                [5, 5, 5], 
                                                [100, 100, 100]),
        num_iterations=10,
        num_samples=1000
    ))
