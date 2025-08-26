from marginal_value import calculate_marginal_value
from sample_valuations import SampleValuations

def local_bid(goods, valuation_function, price_vector, num_iterations=100):
    """
    Use local bid to iteratively set the bid vectors to our marginal values 

    TODO: Fill in local bid as described in the pseudocode in the assignment.
    
    Algorithm 2: LocalBid
    INPUTS: Set of goods G, valuation function v, price vector q
    HYPERPARAMETERS: NUM_ITERATIONS
    OUTPUT: Optimized bid vector
    
    Initialize bid vector b_old with a bid for each good in G
    for NUM_ITERATIONS or until convergence do
        b_new ← b_old.copy()
        for each gk ∈ G do
            MV ← CalcMarginalValue(G, gk, v, b_old, q)
            b_k ← MV
        end for
        b_old ← UpdateBidVector(b_old, b_new)
    end for
    return b_old
    """
    
    # TODO: Implement LocalBid algorithm according to Algorithm 2
    raise NotImplementedError("Implement LocalBid algorithm")

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