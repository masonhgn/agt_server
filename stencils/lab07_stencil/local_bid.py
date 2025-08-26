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