# CS1440/2440 Lab 7: Simultaneous Auctions (Part 2)

## Introduction

Welcome to Lab 7! In this lab, you'll upgrade your auction agent by combining price prediction with the optimization method from last week. Your agent will learn to predict opponents' bids through self-play and use these insights to compute expected marginal values, allowing it to adjust bids dynamically over time.

## Overview

This lab builds on Lab 6 by introducing:
- **Histogram-based price prediction** - Learning opponent bid distributions
- **Expected marginal value calculation** - Computing marginal values over price distributions  
- **Self-play training** - Learning through playing against copies of itself
- **SCPP Agent** - Self-Consistent Price Prediction agent

## Key Concepts

### Price Prediction with Histograms
Instead of assuming fixed prices, your agent will learn to predict what prices opponents will bid using histograms. This allows for more sophisticated bidding strategies.

### Expected Marginal Value
Rather than calculating marginal value for a single price vector, you'll compute the expected marginal value over a distribution of possible prices.

### Self-Consistent Learning
The agent learns by playing against copies of itself, creating a self-consistent prediction of opponent behavior.

## Files in this Stencil

### Core Implementation Files
- `single_good_histogram.py` - **TODO**: Implement histogram operations for single goods
- `independent_histogram.py` - Manages histograms for multiple goods (provided)
- `marginal_value.py` - **TODO**: Implement expected marginal value calculation
- `localbid.py` - **TODO**: Implement expected local bidding algorithm
- `scpp_agent.py` - **TODO**: Implement the SCPP agent with self-play learning
- `competition_agent.py` - **TODO**: Implement your competition agent

### Additional Files
- `example_solutions.py` - Example implementations for reference
- `run_tests.py` - Test runner for all components
- `requirements.txt` - Python dependencies

## Implementation Guide

### Step 1: Single Good Histogram
Implement the `SingleGoodHistogram` class methods:
- `add_record(price)` - Add a price observation to the histogram
- `smooth(alpha)` - Smooth the histogram using exponential decay
- `update(new_hist, alpha)` - Update with new histogram data
- `sample()` - Sample a price from the histogram distribution

### Step 2: Expected Marginal Value
Implement `calculate_expected_marginal_value()`:
- Sample multiple price vectors from the distribution
- Calculate marginal value for each sample
- Return the average marginal value

### Step 3: Expected Local Bidding
Implement `expected_local_bid()`:
- Similar to local bidding from Lab 6
- But uses expected marginal values instead of fixed prices
- Iteratively updates bids based on price distribution

### Step 4: SCPP Agent
Implement the SCPP agent:
- `get_bids()` - Use expected local bidding
- `update()` - Learn from opponent bids and update histograms
- Self-play training mode for learning

### Step 5: Competition Agent
Create your final competition agent that combines all techniques.

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tests**:
   ```bash
   python run_tests.py
   ```

3. **Implement the stencils** in order:
   - Start with `single_good_histogram.py`
   - Then `marginal_value.py`
   - Then `localbid.py`
   - Then `scpp_agent.py`
   - Finally `competition_agent.py`

## Example Usage

```python
from single_good_histogram import SingleGoodHistogram
from marginal_value import calculate_expected_marginal_value
from localbid import expected_local_bid

# Create a histogram
hist = SingleGoodHistogram(bucket_size=5, bid_upper_bound=100)

# Add some observations
hist.add_record(25)
hist.add_record(30)
hist.add_record(35)

# Sample from the distribution
price = hist.sample()

# Use in expected marginal value calculation
expected_mv = calculate_expected_marginal_value(
    goods={"A", "B"}, 
    selected_good="A",
    valuation_function=lambda bundle: len(bundle) * 10,
    bids={"A": 20, "B": 15},
    price_distribution=hist,
    num_samples=50
)
```

## Training and Testing

### Training Mode
```bash
python scpp_agent.py --mode TRAIN --num_rounds 1000
```

### Testing Mode
```bash
python scpp_agent.py --mode RUN
```

### Competition Agent
```bash
python competition_agent.py
```

## Key Algorithms

### Histogram Smoothing
```python
def smooth(self, alpha):
    # For each bucket, apply exponential decay
    # new_frequency = (1 - alpha) * old_frequency + alpha * uniform_frequency
```

### Expected Marginal Value
```python
def calculate_expected_marginal_value(goods, selected_good, valuation_function, bids, price_distribution, num_samples=50):
    total_mv = 0
    for _ in range(num_samples):
        prices = price_distribution.sample()
        mv = calculate_marginal_value(goods, selected_good, valuation_function, bids, prices)
        total_mv += mv
    return total_mv / num_samples
```

## Tips

1. **Start simple**: Begin with basic histogram operations before moving to complex algorithms.

2. **Test incrementally**: Test each component separately before integrating.

3. **Understand the math**: Make sure you understand the expected value calculations.

4. **Use the example solutions**: Check `example_solutions.py` if you get stuck.

5. **Experiment with parameters**: Try different values for alpha, bucket sizes, and sample counts.

## Grading

Your implementation will be tested on:
- Correctness of histogram operations
- Accuracy of expected marginal value calculations
- Performance of the SCPP agent in self-play
- Quality of the competition agent
- Code style and documentation

## Submission

Submit your completed implementations of:
- `single_good_histogram.py`
- `marginal_value.py`
- `localbid.py`
- `scpp_agent.py`
- `competition_agent.py`

Make sure all stencils are properly implemented and tested before submission. 