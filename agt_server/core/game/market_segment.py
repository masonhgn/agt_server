from enum import Enum

class MarketSegment(Enum):
    MALE = "Male"
    FEMALE = "Female"
    YOUNG = "Young"
    OLD = "Old"
    LOW_INCOME = "LowIncome"
    HIGH_INCOME = "HighIncome"
    MALE_YOUNG = "Male_Young"
    MALE_OLD = "Male_Old"
    MALE_LOW_INCOME = "Male_LowIncome"
    MALE_HIGH_INCOME = "Male_HighIncome"
    FEMALE_YOUNG = "Female_Young"
    FEMALE_OLD = "Female_Old"
    FEMALE_LOW_INCOME = "Female_LowIncome"
    FEMALE_HIGH_INCOME = "Female_HighIncome"
    YOUNG_LOW_INCOME = "Young_LowIncome"
    YOUNG_HIGH_INCOME = "Young_HighIncome"
    OLD_LOW_INCOME = "Old_LowIncome"
    OLD_HIGH_INCOME = "Old_HighIncome"
    MALE_YOUNG_LOW_INCOME = "Male_Young_LowIncome"
    MALE_YOUNG_HIGH_INCOME = "Male_Young_HighIncome"
    MALE_OLD_LOW_INCOME = "Male_Old_LowIncome"
    MALE_OLD_HIGH_INCOME = "Male_Old_HighIncome"
    FEMALE_YOUNG_LOW_INCOME = "Female_Young_LowIncome"
    FEMALE_YOUNG_HIGH_INCOME = "Female_Young_HighIncome"
    FEMALE_OLD_LOW_INCOME = "Female_Old_LowIncome"
    FEMALE_OLD_HIGH_INCOME = "Female_Old_HighIncome"

    @classmethod
    def all_segments(cls):
        return list(cls)

    @classmethod
    def is_subset(cls, campaign_segment, user_segment):
        attrs1 = set(campaign_segment.value.split('_'))
        attrs2 = set(user_segment.value.split('_'))
        return attrs2.issubset(attrs1) 