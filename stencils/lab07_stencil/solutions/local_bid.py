from marginal_values import calculate_expected_marginal_value
from independent_histogram import IndependentHistogram


def expected_local_bid(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
    """
    Iteratively computes a bid vector by updating bids to be the expected marginal value for each good.
    """
    # TODO: Implement LocalBid with price sampling according to Algorithm 2
    raise NotImplementedError("Implement LocalBid with price sampling")

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
    
    print(expected_local_bid(
        goods=["a", "b", "c"],
        valuation_function=valuation,
        price_distribution=IndependentHistogram(["a", "b", "c"], 
                                                [5, 5, 5], 
                                                [100, 100, 100]),
        num_iterations=10,
        num_samples=1000
    )) 