import random

class SingleGoodHistogram:
    def __init__(self, bucket_size, bid_upper_bound):
        self.bucket_size = bucket_size
        self.bid_upper_bound = bid_upper_bound
        self.buckets = {}
        for b in range(0, bid_upper_bound, bucket_size):
            self.buckets[b] = 0.0
        self.total = 0.0

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
        # TODO: Implement add_record method
        # 1. Get the bucket for the price using self.get_bucket(price)
        # 2. Increment the frequency of that bucket
        # 3. Increment the total frequency
        raise NotImplementedError("Implement add_record method")

    def smooth(self, alpha):
        """
        Smooth the histogram using the technique described in the handout.
        """
        # TODO: Implement smooth method
        # Iterate over each bucket and multiply its frequency by (1 - alpha)
        raise NotImplementedError("Implement smooth method")

    def update(self, new_hist, alpha):
        """ 
        Actually updating the histogram with new information: 
        1. Smooth the current histogram.
        2. Add the new histogram to the current histogram.
        """
        # TODO: Implement update method
        # 1. Smooth the current histogram using self.smooth(alpha)
        # 2. For each bucket, increase its frequency by alpha times the corresponding frequency in new_hist
        raise NotImplementedError("Implement update method")

    def sample(self):
        """ 
        Return a random sample from the histogram. 
        """
        # TODO: Implement sample method
        # Generate a random number z between 0 and 1, and return the value at the zth-percentile
        # To avoid sampling from an empty histogram, you can initialize all bucket counts to 1
        raise NotImplementedError("Implement sample method")

    
    def __repr__(self):
        return str(self.buckets) 