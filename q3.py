"""Project 3 Q3."""
from classes import Player, Table


def phasedout_is_valid_play(play, player_id, table, turn_history, phase_status,
                            hand, discard):
    """phasedout_is_valid_play returns validity of "play" given game status."""
    curr_player = Player(player_id, phase_status[player_id], hand)
    stats = Table(table, turn_history, phase_status, discard)
    return stats.check_play(play, curr_player)


if __name__ == '__main__':
    # Example calls to the function.
    print(phasedout_is_valid_play((3, [['2S', '2S', '2C'],
                                       ['AS', '5S', '5S']]),
                                  0,
                                  [(None, []), (None, []),
                                   (None, []), (None, [])],
                                  [(0, [(2, 'JS')])],
                                  [0, 0, 0, 0], ['AS', '2S', '2S', '2C',
                                                 '5S', '5S', '7S', '8S',
                                                 '9S', '0S', 'JS'],
                                  None))
    print(phasedout_is_valid_play((4, ('KC', (1, 0, 0))),
                                  1,
                                  [(None, []), (2, [['2S', '2S', 'AS', '5S',
                                                     '5S', '7S', 'JS']]),
                                   (None, []), (None, [])],
                                  [(0, [(2, 'JS'), (5, 'JS')]),
                                   (1, [(1, 'XX'), (3, [['2S', '2S', 'AS',
                                                         '5S', '5S', '7S',
                                                         'JS']])])],
                                  [0, 2, 0, 0],
                                  ['5D', '0S', 'JS', 'KC'],
                                  '0H'))
    print(phasedout_is_valid_play((5, 'JS'),
                                  1,
                                  [(None, []), (1, [['2S', '2S', '2C'],
                                                    ['AS', '5S', '5S']]),
                                   (None, []), (None, [])],
                                  [(0, [(2, 'JS'), (5, 'JS')]),
                                   (1, [(1, 'XX'),
                                        (3, [['2S', '2S', '2C'],
                                             ['AS', '5S', '5S']])])],
                                  [0, 1, 0, 0],
                                  ['AD', '8S', '9S', '0S', 'JS'],
                                  '3C'))
