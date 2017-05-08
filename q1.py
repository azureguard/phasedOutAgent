"""Project 3 Q1."""
from classes import Group


def phasedout_group_type(group):
    """phasedout_group_type returns the group type of a list of cards."""
    return Group(group).group


if __name__ == '__main__':
    # Example calls to the function.
    print(phasedout_group_type(['2C', '2S', '2H']))
    print(phasedout_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']))
    print(phasedout_group_type(['4H', '4S', 'AC', '4C']))
    print(phasedout_group_type(
        ['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']))
    print(phasedout_group_type(['4H', '5D', 'AC', '7H']))
    print(phasedout_group_type(['4H', '5D', '7C', 'AC']))
