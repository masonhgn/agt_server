import random
import itertools

class SampleValuations:
    """Defines different valuation functions, including additive, complement, and substitute valuations."""
    
    SINGLE_ITEM_VALS = {
        "A": 70.0, "B": 55.0, "C": 85.0, "D": 50.0, "E": 15.0,
        "F": 65.0, "G": 80.0, "H": 90.0, "I": 75.0, "J": 60.0,
        "K": 40.0, "L": 80.0, "M": 90.0, "N": 25.0, "O": 65.0, "P": 70.0
    }

    COMPLEMENTS = {}
    SUBSTITUTES = {}

    @staticmethod
    def additive_valuation(bundle):
        return sum(SampleValuations.SINGLE_ITEM_VALS.get(item, 0) for item in bundle)

    @staticmethod
    def complement_valuation(bundle):
        base_value = SampleValuations.additive_valuation(bundle)
        complement_multiplier = 1.2 ** (len(bundle) - 1)
        return base_value * complement_multiplier if bundle else 0

    @staticmethod
    def substitute_valuation(bundle):
        base_value = SampleValuations.additive_valuation(bundle)
        substitute_multiplier = 0.8 ** (len(bundle) - 1)
        return base_value * substitute_multiplier if bundle else 0

    @staticmethod
    def randomized_valuation(bundle):
        base_value = SampleValuations.additive_valuation(bundle)
        
        if len(bundle) < 2:
            return base_value

        key = tuple(sorted(bundle))
        if key in SampleValuations.COMPLEMENTS:
            return base_value * SampleValuations.COMPLEMENTS[key]
        elif key in SampleValuations.SUBSTITUTES:
            return base_value * SampleValuations.SUBSTITUTES[key]
        return base_value

    @staticmethod
    def generate_complements_and_substitutes():
        items = list(SampleValuations.SINGLE_ITEM_VALS.keys())

        for k in range(2, len(items) + 1):
            for subset in itertools.combinations(items, k):
                modifier = 1.0 - random.uniform(0.0, 0.001)
                if random.random() < 0.5:
                    SampleValuations.SUBSTITUTES[subset] = modifier
                else:
                    SampleValuations.COMPLEMENTS[subset] = 1.0 / modifier

    @staticmethod
    def generate_price_vector():
        return {item: random.uniform(value - 7.5, value + 7.5) for item, value in SampleValuations.SINGLE_ITEM_VALS.items()}


SampleValuations.generate_complements_and_substitutes() 