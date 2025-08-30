"""
Solution for marginal values implementation.
"""

def calculate_marginal_value(goods, selected_good, valuation_function, bids, prices):
    """
    Compute the marginal value of selected_good: 
    the difference between the valuation of the bundle that includes the good and the bundle without it.
    A bidder wins a good if bid >= price.
    """
    # Determine which goods you would win with current bids
    won_goods = set()
    for good in goods:
        if good != selected_good and bids.get(good, 0) >= prices.get(good, 0):
            won_goods.add(good)
    
    # Value with the selected good
    bundle_with_good = won_goods | {selected_good}
    value_with_good = valuation_function(bundle_with_good)
    
    # Value without the selected good
    bundle_without_good = won_goods
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
        for gk ∈ G\{gj} do
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
        # Sample a price vector
        prices = price_distribution.sample()
        
        # Determine which goods you would win with current bids
        bundle = set()
        for good in goods:
            if good != selected_good:
                price = prices.get(good, 0)
                bid = bids.get(good, 0)
                if bid > price:
                    bundle.add(good)
        
        # Calculate marginal value for this sample
        bundle_with_good = bundle | {selected_good}
        bundle_without_good = bundle
        mv = valuation_function(bundle_with_good) - valuation_function(bundle_without_good)
        total_mv += mv
    
    # Return average marginal value
    avg_mv = total_mv / num_samples
    return avg_mv
