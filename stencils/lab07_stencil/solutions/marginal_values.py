"""
Solution for marginal values implementation.
"""

import random

def calculate_marginal_value(goods, selected_good, valuation_function, bids, prices):
    """
    Compute the marginal value of selected_good: 
    the difference between the valuation of the bundle that includes the good and the bundle without it.
    A bidder wins a good if bid >= price.
    """
    # Determine which goods the bidder would win with current bids
    won_goods = set()
    for good in goods:
        if bids.get(good, 0) >= prices.get(good, 0):
            won_goods.add(good)
    
    # Value with the selected good
    bundle_with_good = won_goods | {selected_good}
    value_with_good = valuation_function(bundle_with_good)
    
    # Value without the selected good
    bundle_without_good = won_goods - {selected_good}
    value_without_good = valuation_function(bundle_without_good)
    
    # Marginal value is the difference
    marginal_value = value_with_good - value_without_good
    
    return marginal_value

def calculate_expected_marginal_value(goods, selected_good, valuation_function, bids, price_distribution, num_samples=50):
    """
    Compute the expected marginal value of selected_good:
    the average of the marginal values over a number of samples.
    
    Algorithm 1: Estimate the expected marginal value of good gj
    INPUTS: Set of goods G, select good gj ∈ G, valuation function v, bid vector b, price distribution P
    HYPERPARAMETERS: NUM_SAMPLES
    OUTPUT: An estimate of the expected marginal value of good gj
    
    totalMV ← 0
    for NUM_SAMPLES do
        p ← P.sample()
        bundle ← {}
        for gk ∈ G\\{gj} do
            price ← pk
            bid ← bk
            if bid > price then
                bundle.Add(gk)
            end if
        end for
        totalMV += [v(bundle ∪ {gj}) - v(bundle)]
    end for
    avgMV ← totalMV / NUM_SAMPLES
    return avgMV
    """
    total_mv = 0
    
    for _ in range(num_samples):
        # Sample a price vector from the distribution
        p = price_distribution.sample()
        
        # Determine which goods the bidder would win (excluding the selected good)
        bundle = set()
        for gk in goods - {selected_good}:
            price = p.get(gk, 0)
            bid = bids.get(gk, 0)
            if bid > price:
                bundle.add(gk)
        
        # Calculate marginal value for this sample
        value_with_good = valuation_function(bundle | {selected_good})
        value_without_good = valuation_function(bundle)
        marginal_value = value_with_good - value_without_good
        
        total_mv += marginal_value
    
    # Return the average
    return total_mv / num_samples
