from marginal_value import calculate_marginal_value
from sample_valuations import SampleValuations

def local_bid(goods, valuation_function, price_vector, num_iterations=100):
    """
    Use local bid to iteratively set the bid vectors to our marginal values 

    TODO: Fill in local bid as described in the pseudocode in the assignment.
    """
    
    # TODO: Implement LocalBid algorithm according to Algorithm 2
    bid_vector = {good: 0 for good in goods}

    for _ in range(num_iterations):
        new_bid_vector = bid_vector.copy()
        for good in goods:
            marginal_value = calculate_marginal_value(goods, good, valuation_function, bid_vector, price_vector)
            new_bid_vector[good] = marginal_value
        bid_vector = new_bid_vector

    return bid_vector

if __name__ == "__main__":
    goods = set(SampleValuations.SINGLE_ITEM_VALS.keys())
    price_vector = SampleValuations.generate_price_vector() 

    for valuation_func in [
        SampleValuations.additive_valuation,
        SampleValuations.complement_valuation,
        SampleValuations.substitute_valuation,
        SampleValuations.randomized_valuation
    ]:
        print(f"Running LocalBid with {valuation_func.__name__}:")
        optimized_bids = local_bid(goods, valuation_func, price_vector, num_iterations=100)
        print("Final bid vector:", optimized_bids, "\n") 