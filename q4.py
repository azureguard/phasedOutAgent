"""Project 3 Q4."""
from classes import Player


def phasedout_score(hand):
    """phasedout_score counts the points in given hand."""
    return Player(0, 0, hand).score


if __name__ == '__main__':
    # Example calls to the function.
    print(phasedout_score(['9D', '9S', '9D', '0D', '0S', '0D']))
    print(phasedout_score(['2D', '9S', 'AD', '0D']))
    print(phasedout_score([]))
