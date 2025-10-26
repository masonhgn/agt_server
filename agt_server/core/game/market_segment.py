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
    def is_subset(cls, subset_segment, superset_segment):
        """
        Check if subset_segment is a subset of superset_segment.
        Returns True if all attributes in subset_segment are also in superset_segment.
        
        Examples:
        - is_subset(Female_Old_HighIncome, Female_Old) = True
        - is_subset(Female_Old, Female_Old_HighIncome) = False
        """
        subset_attrs = set(subset_segment.value.split('_'))
        superset_attrs = set(superset_segment.value.split('_'))
        return subset_attrs.issubset(superset_attrs)
    
    @classmethod
    def can_serve(cls, bid_entry_segment, user_segment):
        """
        Check if a bid entry can serve a user.
        Returns True if the user segment contains all attributes of the bid entry segment.
        
        Examples:
        - can_serve(Female_Old, Female_Old_HighIncome) = True (can serve)
        - can_serve(Female_Old_HighIncome, Female_Old) = False (cannot serve)
        """
        bid_attrs = set(bid_entry_segment.value.split('_'))
        user_attrs = set(user_segment.value.split('_'))
        return bid_attrs.issubset(user_attrs)
    
    @classmethod
    def matches_campaign(cls, bid_entry_segment, campaign_segment):
        """
        Check if a bid entry matches a campaign.
        Returns True if the bid entry segment contains all attributes of the campaign segment.
        
        Examples:
        - matches_campaign(Female_Old_HighIncome, Female_Old) = True (matches)
        - matches_campaign(Female_Old, Female_Old_HighIncome) = False (doesn't match)
        """
        campaign_attrs = set(campaign_segment.value.split('_'))
        bid_attrs = set(bid_entry_segment.value.split('_'))
        return campaign_attrs.issubset(bid_attrs) 

    


    