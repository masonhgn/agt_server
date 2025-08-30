def calculate_marginal_value(goods, selected_good, valuation_function, bids, prices):
    """
    Calculates the marginal value of a given good for a bidder in a simultaneous sealed bid auction.

    TODO: Fill in marginal value as described in the pseudocode in the assignment.
    """
    won_goods = {good for good in goods if bids[good] >= prices[good] and good != selected_good}
    valuation_without_selected = valuation_function(won_goods)

    won_goods_with_selected = won_goods | {selected_good}
    valuation_with_selected = valuation_function(won_goods_with_selected)

    marginal_value = valuation_with_selected - valuation_without_selected
    return marginal_value
