# CS1440/2440 Lab 6: Simultaneous Auctions (Part 1)

## Introduction
This lab introduces you to the concept of marginal values and how to use them to optimize your bids in a simple Simultaneous Sealed Bid Auction. Later labs will build off of these ideas, so please make sure to understand this material well.

## Overview
In a simultaneous sealed bid auction, multiple goods are auctioned simultaneously. Each player submits bids for all goods, and each good is awarded to the highest bidder who pays their bid amount. The key insight is understanding the marginal value of each good - how much additional value a good provides given what you already have.

## Files in this Stencil

### Core Files
- `marginal_value.py` - **TODO**: Implement the `calculate_marginal_value` function
- `localbid.py` - **TODO**: Implement the `local_bid` function for iterative bidding optimization
- `sample_valuations.py` - Contains different valuation functions (additive, complement, substitute, randomized)
- `test_marginal_value.py` - Test cases for your marginal value implementation

### Additional Files
- `example_solutions.py` - Example implementations for reference
- `run_tests.py` - Script to run all tests
- `requirements.txt` - Python dependencies

## Key Concepts

### Marginal Value
The marginal value of a good is the additional value it provides given your current bundle. It's calculated as:
```
marginal_value = value(bundle_with_good) - value(bundle_without_good)
```

### Local Bidding
Local bidding is an iterative algorithm that:
1. Starts with some initial bid vector
2. For each good, calculates the marginal value
3. Updates the bid to match the marginal value
4. Repeats until convergence

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tests**:
   ```bash
   python run_tests.py
   ```

3. **Implement the stencils**:
   - Start with `marginal_value.py`
   - Then implement `localbid.py`
   - Add your own test cases to `test_marginal_value.py`

## Example Usage

```python
from sample_valuations import SampleValuations
from marginal_value import calculate_marginal_value

# Define goods and valuation
goods = {"A", "B", "C"}
valuation = SampleValuations.additive_valuation

# Current bids and prices
bids = {"A": 50, "B": 30, "C": 40}
prices = {"A": 45, "B": 25, "C": 35}

# Calculate marginal value for good A
mv_a = calculate_marginal_value(goods, "A", valuation, bids, prices)
print(f"Marginal value of A: {mv_a}")
```

## Testing

The test file includes:
- An example case with known expected values
- A case where no goods are won
- Three placeholder test cases for you to fill in

Run tests with:
```bash
python -m unittest test_marginal_value.py
```

## Submission

Submit your completed implementations of:
- `marginal_value.py`
- `localbid.py`
- `test_marginal_value.py` (with your test cases filled in)

## Tips

1. **Understand the marginal value concept**: Think about what goods you would win with your current bids, then calculate the additional value of the selected good.

2. **Test with simple cases first**: Start with additive valuations where goods have independent values.

3. **Consider edge cases**: What happens when you win no goods? What happens when you win all goods?

4. **Use the example solutions**: Check `example_solutions.py` if you get stuck, but try to implement it yourself first.

## Grading

Your implementation will be tested on:
- Correctness of marginal value calculations
- Proper implementation of local bidding algorithm
- Quality of your test cases
- Code style and documentation 