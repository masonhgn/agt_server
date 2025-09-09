"""
Solution for single good histogram implementation.
"""

import random

class SingleGoodHistogram:
    def __init__(self, bucket_size, bid_upper_bound):
        self.bucket_size = bucket_size
        self.bid_upper_bound = bid_upper_bound
        self.buckets = {}
        for b in range(0, bid_upper_bound, bucket_size):
            self.buckets[b] = 1.0  # Initialize with 1 to avoid empty histogram issues
        self.total = sum(self.buckets.values())

    def get_bucket(self, price):
        bucket = int(price // self.bucket_size) * self.bucket_size
        if bucket > self.bid_upper_bound:
            bucket = self.bid_upper_bound
        return bucket

    def add_record(self, price):
        """
        Add a price to the histogram.
        Increment the frequency of the bucket that contains the price.
        """
        bucket = self.get_bucket(price)
        self.buckets[bucket] += 1.0
        self.total += 1.0

    def smooth(self, alpha):
        """
        Smooth the histogram using the technique described in the handout.
        """
        for bucket in self.buckets:
            self.buckets[bucket] *= (1 - alpha)

    def update(self, new_hist, alpha):
        """ 
        Actually updating the histogram with new information: 
        1. Smooth the current histogram.
        2. Add the new histogram to the current histogram.
        """
        self.smooth(alpha)
        for bucket in self.buckets:
            self.buckets[bucket] += alpha * new_hist.buckets[bucket]

    def sample(self):
        """ 
        Return a random sample from the histogram. 
        """
        if self.total == 0:
            return random.uniform(0, self.bid_upper_bound)
        
        # Generate a random number between 0 and 1
        z = random.random()
        cumulative = 0
        
        # Find the bucket at the zth percentile
        for bucket in sorted(self.buckets.keys()):
            cumulative += self.buckets[bucket] / self.total
            if cumulative >= z:
                # Return a random value within the bucket
                return bucket + random.uniform(0, self.bucket_size)
        
        # Fallback: return a value from the last bucket
        return self.bid_upper_bound

    
    def __repr__(self):
        return str(self.buckets)
