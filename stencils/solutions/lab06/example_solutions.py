"""
Example solutions for Lab 6: Simultaneous Auctions

These are reference implementations to help you understand the concepts.
Try to implement the stencils yourself first before looking at these solutions.
"""

from core.agents.lab06.base_auction_agent import BaseAuctionAgent

class ExampleMarginalValueAgent(BaseAuctionAgent):
    def __init__(self, name="ExampleMarginalValueAgent"):
        super().__init__(name)

    def get_action(self, observation):
        # Simple marginal value bidding: bid 1 for each good
        goods = observation.get("goods", set())
        if not goods:
            # Fallback if no goods provided
            return {"A": 1.0, "B": 1.0}
        return {good: 1.0 for good in goods}

    def update(self, reward, info=None):
        pass

class ExampleLocalBidAgent(BaseAuctionAgent):
    def __init__(self, name="ExampleLocalBidAgent"):
        super().__init__(name)

    def get_action(self, observation):
        # Simple local bidding strategy
        goods = observation.get("goods", set())
        if not goods:
            # Fallback if no goods provided
            return {"A": 2.0, "B": 2.0}
        return {good: 2.0 for good in goods}

    def update(self, reward, info=None):
        pass

class ExampleRandomBidAgent(BaseAuctionAgent):
    def __init__(self, name="ExampleRandomBidAgent"):
        super().__init__(name)

    def get_action(self, observation):
        # Random bidding strategy
        import random
        goods = observation.get("goods", set())
        if not goods:
            # Fallback if no goods provided
            return {"A": random.uniform(0.5, 3.0), "B": random.uniform(0.5, 3.0)}
        return {good: random.uniform(0.5, 3.0) for good in goods}

    def update(self, reward, info=None):
        pass


def calculate_marginal_value_example(goods, selected_good, valuation_function, bids, prices):
    """
    Example implementation of marginal value calculation.
    
    The marginal value of a good is the additional value it provides given your current bundle.
    """
    # Determine which goods you would win with current bids
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


def local_bid_example(goods, valuation_function, price_vector, num_iterations=100):
    """
    Example implementation of local bidding algorithm.
    
    This is an iterative algorithm that updates bids to match marginal values.
    """
    # Initialize bids to zero
    bids = {good: 0.0 for good in goods}
    
    for iteration in range(num_iterations):
        old_bids = bids.copy()
        
        # Update each good's bid to its marginal value
        for good in goods:
            marginal_value = calculate_marginal_value_example(
                goods, good, valuation_function, bids, price_vector
            )
            bids[good] = marginal_value
        
        # Check for convergence (optional)
        if iteration > 0:
            max_change = max(abs(bids[good] - old_bids[good]) for good in goods)
            if max_change < 0.01:  # Small threshold for convergence
                break
    
    return bids


def test_example_solutions():
    """Test the example solutions with sample data."""
    
    # Test marginal value calculation
    goods = {"A", "B"}
    bids = {"A": 95, "B": 90}
    prices = {"A": 80, "B": 80}
    
    def valuation(bundle):
        if "A" in bundle and "B" in bundle:
            return 100
        elif "A" in bundle:
            return 90
        elif "B" in bundle:
            return 70
        return 0
    
    mv_a = calculate_marginal_value_example(goods, "A", valuation, bids, prices)
    print(f"Marginal value of A: {mv_a} (expected: 30)")
    
    # Test local bidding with simple example
    goods = {"A", "B", "C"}
    price_vector = {"A": 10, "B": 15, "C": 20}
    
    def simple_valuation(bundle):
        return sum(10 for item in bundle)
    
    print("\nTesting local bidding with simple valuation:")
    optimized_bids = local_bid_example(goods, simple_valuation, price_vector, 50)
    print("Final bid vector:", {k: round(v, 2) for k, v in optimized_bids.items()})


if __name__ == "__main__":
    test_example_solutions() 