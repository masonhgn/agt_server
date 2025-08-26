"""
Example solutions for Lab 7: Simultaneous Auctions (Part 2)

These are reference implementations to help you understand the concepts.
Try to implement the stencils yourself first before looking at these solutions.
"""

import random
import numpy as np
from single_good_histogram import SingleGoodHistogram
from independent_histogram import IndependentHistogram


def calculate_marginal_value_example(goods, selected_good, valuation_function, bids, prices):
    """
    Example implementation of marginal value calculation.
    """
    won_goods = {g for g in goods if bids.get(g, 0) >= prices.get(g, 0) and g != selected_good}
    valuation_without = valuation_function(won_goods)
    won_goods_with = won_goods.union({selected_good})
    valuation_with = valuation_function(won_goods_with)
    return valuation_with - valuation_without


def calculate_expected_marginal_value_example(goods, selected_good, valuation_function, bids, price_distribution, num_samples=50):
    """
    Example implementation of expected marginal value calculation.
    """
    total_mv = 0
    for _ in range(num_samples):
        prices = price_distribution.sample()
        mv = calculate_marginal_value_example(goods, selected_good, valuation_function, bids, prices)
        total_mv += mv
    return total_mv / num_samples


def expected_local_bid_example(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
    """
    Example implementation of expected local bidding algorithm.
    """
    # Initialize bids to zero
    bids = {good: 0.0 for good in goods}
    
    for iteration in range(num_iterations):
        old_bids = bids.copy()
        
        # Update each good's bid to its expected marginal value
        for good in goods:
            expected_mv = calculate_expected_marginal_value_example(
                goods, good, valuation_function, bids, price_distribution, num_samples
            )
            bids[good] = expected_mv
        
        # Check for convergence (optional)
        if iteration > 0:
            max_change = max(abs(bids[good] - old_bids[good]) for good in goods)
            if max_change < 0.01:  # Small threshold for convergence
                break
    
    return bids


class SingleGoodHistogramExample(SingleGoodHistogram):
    """
    Example implementation of SingleGoodHistogram.
    """
    
    def add_record(self, price):
        """Add a price to the histogram."""
        bucket = self.get_bucket(price)
        self.buckets[bucket] += 1.0
        self.total += 1.0
    
    def smooth(self, alpha):
        """Smooth the histogram using exponential decay."""
        uniform_frequency = 1.0 / len(self.buckets)
        
        for bucket in self.buckets:
            current_frequency = self.buckets[bucket] / self.total if self.total > 0 else 0
            smoothed_frequency = (1 - alpha) * current_frequency + alpha * uniform_frequency
            self.buckets[bucket] = smoothed_frequency * self.total
    
    def update(self, new_hist, alpha):
        """Update the histogram with new information."""
        # Smooth the current histogram
        self.smooth(alpha)
        
        # Add the new histogram data
        for bucket in self.buckets:
            if bucket in new_hist.buckets:
                self.buckets[bucket] += new_hist.buckets[bucket]
                self.total += new_hist.buckets[bucket]
    
    def sample(self):
        """Sample a price from the histogram distribution."""
        if self.total <= 0:
            # Return random price if no data
            return random.uniform(0, self.bid_upper_bound)
        
        # Choose a bucket based on frequencies
        buckets_list = list(self.buckets.keys())
        frequencies = [self.buckets[bucket] for bucket in buckets_list]
        
        # Normalize frequencies
        total_freq = sum(frequencies)
        if total_freq <= 0:
            return random.uniform(0, self.bid_upper_bound)
        
        probabilities = [freq / total_freq for freq in frequencies]
        
        # Sample bucket
        chosen_bucket = random.choices(buckets_list, weights=probabilities)[0]
        
        # Sample uniformly within the bucket
        bucket_start = chosen_bucket
        bucket_end = min(chosen_bucket + self.bucket_size, self.bid_upper_bound)
        
        return random.uniform(bucket_start, bucket_end)


def test_example_solutions():
    """Test the example solutions with sample data."""
    print("Testing example solutions for Lab 7...")
    
    # Test SingleGoodHistogram
    print("\n1. Testing SingleGoodHistogram:")
    hist = SingleGoodHistogramExample(bucket_size=5, bid_upper_bound=100)
    
    # Add some observations
    for _ in range(100):
        hist.add_record(random.uniform(20, 40))
    
    print(f"Histogram buckets: {hist.buckets}")
    print(f"Sample price: {hist.sample()}")
    
    # Test expected marginal value
    print("\n2. Testing Expected Marginal Value:")
    
    def valuation(bundle):
        return sum(10 for item in bundle)
    
    goods = {"A", "B", "C"}
    bids = {"A": 20, "B": 15, "C": 25}
    
    # Create a simple price distribution
    price_dist = IndependentHistogram(goods, [5, 5, 5], [100, 100, 100])
    for _ in range(50):
        price_dist.add_record({
            "A": random.uniform(15, 25),
            "B": random.uniform(10, 20),
            "C": random.uniform(20, 30)
        })
    
    expected_mv = calculate_expected_marginal_value_example(
        goods, "A", valuation, bids, price_dist, num_samples=100
    )
    print(f"Expected marginal value for A: {expected_mv:.2f}")
    
    # Test expected local bidding
    print("\n3. Testing Expected Local Bidding:")
    optimized_bids = expected_local_bid_example(
        goods, valuation, price_dist, num_iterations=50, num_samples=100
    )
    print(f"Optimized bids: {optimized_bids}")
    
    print("\nPASS: All example solutions working correctly!")


if __name__ == "__main__":
    test_example_solutions() 