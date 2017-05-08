"""Projecr 3 Q5."""
from classes import Player, Table


def phasedout_play(player_id, table, turn_history, phase_status,
                   hand, discard):
    """phasedout_play returns the best or only move given the game status."""
    return False


if __name__ == '__main__':
    # Example call to the function.
    print(phasedout_play(1,
                         [(None, []),
                          (4, [['2C', '3H', '4D', 'AD', '6S', '7C',
                                '8S', '9H', '0S', 'JS']]),
                          (None, []),
                          (None, [])],
                         [(0, [(1, 'JS'), (5, 'JS')]),
                          (1, [(1, 'JS'), (2, [['2C', '3H', '4D', 'AD',
                                                '6S', '7C', '8S', '9H']]),
                               (4, ('0S', (1, 0, 8))),
                               (4, ('JS', (1, 0, 9)))])],
                         [0, 4, 0, 0],
                         ['5D'],
                         '7H'))
