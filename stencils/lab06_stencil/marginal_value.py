def calculate_marginal_value(goods, selected_good, valuation_function, bids, prices):
    """
    Calculates the marginal value of a given good for a bidder in a simultaneous sealed bid auction.

    TODO: Fill in marginal value as described in the pseudocode in the assignment.
    """
    
    # Determine which goods the bidder would win with current bids
    won_goods = set()
    for good in goods:
        if bids[good] >= prices[good]:
            won_goods.add(good)
    
    # Calculate value with the selected good
    bundle_with_good = won_goods | {selected_good}
    value_with_good = valuation_function(bundle_with_good)
    
    # Calculate value without the selected good
    bundle_without_good = won_goods - {selected_good}
    value_without_good = valuation_function(bundle_without_good)
    
    # Marginal value is the difference
    marginal_value = value_with_good - value_without_good
    
    return marginal_value 