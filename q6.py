"""Project 3 Q6."""
import itertools
from collections import defaultdict as dd
from operator import attrgetter

from classes_bonus import Card, Group, Player, Set, Table


def longest_run(player):
    """Get longest natural run to determine hold and discard logic."""
    # initialise collectors
    unique_cards = ([], [])
    card_vals = ([], [])
    longest = [[], []]
    max_length = [0, 0]

    # separate card into colours
    for card in player.hand:
        if not card.value >= 20:
            if card.value not in card_vals[card.colour]:
                unique_cards[card.colour].append(card.name)
                card_vals[card.colour].append(card.value)

    # iterate through all combinations
    curr_colour = -1
    for colour in unique_cards:
        curr_colour += 1
        elements = len(colour)
        # generate slice positions
        for i in range(2, elements + 1):
            for j in range(0, i):
                # do slice and determine length of run
                temp = colour[j:i]
                check_val = [Card(card).value for card in temp]
                length = Group(temp).check_run(check_val)
                # hold longest run length
                if length > max_length[curr_colour]:
                    max_length[curr_colour] = length
                    longest[curr_colour] = temp

    # determine if max length is equal, else hold both coloured runs
    if max_length[0] == max_length[1]:
        l_colour = (0, 1)
    elif max_length[0] > max_length[1]:
        l_colour = (0, )
    else:
        l_colour = (1, )

    return max_length, longest, l_colour


def slice_run(card_list, phase, valid_plays):
    """Get valid runs from slicing generated runs."""
    # set definitions
    elements = len(card_list)
    phase_type = {4: 8, 5: 4}

    # generate slice positions
    for i in range(phase_type[phase], elements + 1):
        # do slice and check group validity given current phase
        temp = card_list[0 + i - phase_type[phase]:i]
        if Group(temp).group == phase:
            valid_plays.append((3, [temp]))

    if len(valid_plays):
        return True


def make_run(unique_cards, wild_cards, phase, valid_plays):
    """Generate valid run sequence for phase 4."""
    # set definitions
    elements = len(unique_cards)
    max_len = elements + len(wild_cards)
    phase_type = {4: 8, 5: 4}
    # check natural without wild first, break on valid runs generated
    if elements >= phase_type[phase]:
        if slice_run(unique_cards, phase, valid_plays):
            return

    # generate positions for wild card insertion
    for wild in range(1, len(wild_cards) + 1):
        if wild + elements >= phase_type[phase]:
            possible_locs = itertools.combinations(range(max_len), wild)
            # generate run for each combination of insertions
            for combinations in possible_locs:
                temp = unique_cards[:]
                wild_card = 0
                for pos in combinations:
                    temp.insert(pos, wild_cards[wild_card])
                    wild_card += 1
                slice_run(temp, phase, valid_plays)


def phase_play(player, table, discard):
    """Return valid groups within hand for specified type."""
    # get current player status
    phases = player.phase
    temp = player.hand_list
    hand = [card for card in temp if not card == 'ZZ']
    # set collector list
    valid_plays = []
    # definitions of groups in phases
    lengths = {1: (6, 3), 2: 7, 3: (8, 4), 5: (8, 4)}
    groups = {1: (1, 1), 2: 2, 3: (3, 3), 5: (5, 3)}

    # try plays for all unplayed phases
    # phase 1 not played
    if phases[0] is False:
        phase = 1
        # generate combinations for each group
        super_set = itertools.combinations(hand, lengths[phase][0])
        for sub_set in super_set:
            for g1 in itertools.combinations(sub_set, lengths[phase][1]):
                # continue only if first group valid
                if Group(list(g1)).group == groups[phase][0]:
                    g1, g2 = list(g1), list(sub_set)
                    # determine second group
                    for card in g1:
                        g2.remove(card)
                    # check second group
                    if Group(g2).group == groups[phase][1]:
                        valid_plays.append((3, [g1, g2]))
    # phase 2 not played
    if phases[1] is False:
        phase = 2
        # generate combinations
        super_set = itertools.combinations(hand, lengths[phase])
        # check group validity
        for g1 in super_set:
            if Group(list(g1)).group == groups[phase]:
                valid_plays.append((3, [list(g1)]))

    # phase 3 not played
    if phases[2] is False:
        phase = 3
        # generate combinations for each group
        super_set = itertools.combinations(hand, lengths[phase][0])
        for sub_set in super_set:
            for g1 in itertools.combinations(sub_set, lengths[phase][1]):
                # continue only if first group valid
                if Group(list(g1)).group == groups[phase][0]:
                    g1, g2 = list(g1), list(sub_set)
                    # determine second group
                    for card in g1:
                        g2.remove(card)
                    # check second group
                    if Group(g2).group == groups[phase][1]:
                        valid_plays.append((3, [g1, g2]))
    # phase 4 not played
    if phases[3] is False:
        phase = 4
        # initialise collector lists
        unique_cards = []
        wild_cards = []
        card_vals = []
        # pre-process hand for run generation
        for card in player.hand:
            if card.value not in card_vals and not card.value == 25:
                if card.name not in unique_cards:
                    unique_cards.append(card.name)
                    card_vals.append(card.value)
            if card.value == 25:
                wild_cards.append(card.name)
        # do run check only when minimum card elements met
        if len(unique_cards) + len(wild_cards) >= 8:
            make_run(unique_cards, wild_cards, phase, valid_plays)

    # phase 5 not played
    if phases[4] is False:
        phase = 5
        # pre-process card list for run generation with collector lists
        unique_cards = ([], [], [])
        card_vals = ([], [], [])
        wild_cards = []
        test_plays = ([], [])

        # split hand into separate colours and wilds
        for card in player.hand:
            if not card.value == 25:
                if card.value not in card_vals[card.colour]:
                    unique_cards[card.colour].append(card.name)
                    card_vals[card.colour].append(card.value)
            if card.value == 25:
                wild_cards.append(card.name)

        # do run check only when minimum card elements met
        if len(unique_cards[0]) + len(wild_cards) >= 4:
            make_run(unique_cards[0], wild_cards, phase, test_plays[0])
        if len(unique_cards[1]) + len(wild_cards) >= 4:
            make_run(unique_cards[1], wild_cards, phase, test_plays[1])

        # for each run, check remainder for valid group 3
        test_plays = test_plays[0] + test_plays[1]
        for play in test_plays:
            g1 = play[1][0]
            curr_hand = hand[:]
            for card in g1:
                curr_hand.remove(card)
            for g2 in itertools.combinations(curr_hand, lengths[phase][1]):
                if Group(list(g2)).group == groups[phase][1]:
                    valid_plays.append((3, [g1, list(g2)]))

    # play set with greatest score
    if len(valid_plays):
        best_score = 0
        for play in valid_plays:
            score = Set(play[1][0]).score
            if score > best_score:
                best_play = play
                best_score = score
        return best_play
    # discard if no valid play
    elif discard[0] is 'ZZ':
        return (6, discard[1])
    else:
        return (5, discard[0])


def gen_4s(hand, table, logical_plays):
    """Generate all possible play locations for each card in hand."""
    for card in hand:
        # for each player with phase played
        pid = 0
        for sets in table.status:
            if sets.phase is not None:
                # for each group in phase
                gid = 0
                for group in sets.group:
                    if group.group is None:
                        break
                    logical_plays.append((4, (card.name, (pid, gid, 0))))
                    logical_plays.append((4, (card.name, (pid, gid,
                                                          len(group.cards)))))
                    gid += 1
            pid += 1


def check_4s(table, logical_plays, valid_plays):
    """Check validity of play, return first valid play."""
    # define group types for each phase
    phase_groups = {
        1: (1, 1),
        2: (2, None),
        3: (3, 3),
        4: (4, None),
        5: (5, 3)
    }
    # iterate through generated plays for validity
    for play in logical_plays:
        pid, gid = play[1][1][0], play[1][1][1]
        card, pos = play[1][0], play[1][1][2]
        phase = table.status[pid].phase
        group_type = phase_groups[phase][gid]
        group_cards = table.status[pid].group[gid].cards
        cards = [card.name for card in group_cards]
        if group_type is None:
            pass
        elif Group(cards, group_type).check_add(pos, card, group_type):
            valid_plays.append(play)


def valid_4s(player, table, discard):
    """Return possible play onto sets, else return best discard."""
    # initialise collector lists
    logical_plays = []
    valid_plays = []
    # generate all possible play locations for each card in hand
    # check validity of play, return first valid play
    gen_4s(player.hand, table, logical_plays)
    check_4s(table, logical_plays, valid_plays)

    # return first valid play, else discard
    if len(valid_plays):
        return valid_plays[0]
    elif discard[0] is 'ZZ':
        return (6, discard[1])
    else:
        return (5, discard[0])


def prob_count(player, table):
    """Get probability of card occurrence."""
    # get current game status and history
    history = table.history
    played = table.status
    # define collector dictionaries and variables
    skip_status = [0, 0, 0, 0]
    deck = 63
    player_hands = {0: 10, 1: 10, 2: 10, 3: 10}
    prob_col = {0: 48, 1: 48, 2: 4}
    suits = ('C', 'D', 'H', 'S', 'Z')
    prob_val = {}
    prob_suit = {}
    for val in range(2, 14):
        prob_val[val] = 8
    prob_val[25] = 8
    prob_val[20] = 4
    for suit in suits:
        prob_suit[suit] = 24

    # iterate through history elements for probability count
    for group in history:
        curr_player = group[0]
        plays = group[1]
        # reset skip status after player skipped
        if curr_player == 0:
            skip_status[3] = 0
        else:
            skip_status[curr_player - 1] = 0

        for play in plays:
            if play[0] == 1:
                player_hands[curr_player] += 1
                deck -= 1

            # additional logic for opponent draws (hand comp prediction)
            if play[0] == 2:
                player_hands[curr_player] += 1
                if ((table.phase_status[curr_player] == 1 or
                     table.phase_status[curr_player] == 3) and
                        not curr_player == player.pid):
                    picked = Card(play[1])
                    prob_val[picked.value] -= 1
                if table.phase_status[curr_player] == 2:
                    picked = Card(play[1])
                    if not picked.value == 25:
                        prob_suit[picked.suit] -= 1

            if play[0] == 3:
                no_cards = 0
                for group in play[1]:
                    no_cards += len(group)
                player_hands[curr_player] -= no_cards

            if play[0] >= 4:
                player_hands[curr_player] -= 1

            if play[0] == 5:
                discarded = Card(play[1])
                if not discarded.value == 25:
                    prob_col[discarded.colour] -= 1
                    prob_suit[discarded.suit] -= 1
                prob_val[discarded.value] -= 1

            if play[0] == 6:
                skip_status[play[1]] = 1

    # get number of cards spent
    for phase in played:
        for card in phase.cards:
            if not card.value == 25:
                prob_col[card.colour] -= 1
                prob_suit[card.suit] -= 1
            prob_val[card.value] -= 1
    for card in player.hand:
        if not card.value == 25:
            prob_col[card.colour] -= 1
            prob_suit[card.suit] -= 1
        prob_val[card.value] -= 1

    # simple probability deduction
    cards_left = sum(player_hands.values()) + deck - len(player.hand)
    for k, v in prob_col.items():
        prob_col[k] = v / cards_left
    for k, v in prob_val.items():
        prob_val[k] = v / cards_left
    for k, v in prob_suit.items():
        prob_suit[k] = v / cards_left

    return prob_col, prob_suit, prob_val, player_hands, skip_status


def card_count(player, table):
    """Count needed cards, cards to discard."""
    # get player status
    phases = player.phase
    played = table.status[player.pid].phase
    # initialise collectors
    counts = {'colour': dd(int), 'suits': dd(int), 'values': dd(int)}
    colour_count = dd(int)
    suit_count = dd(int)
    value_count = dd(int)

    # get composition of hand
    for card in player.hand:
        if not card.value == 25:
            counts['colour'][card.colour] += 1
            counts['suits'][card.suit] += 1
            colour_count[card.colour] += 1
            suit_count[card.suit] += 1
        counts['values'][card.value] += 1
        value_count[card.value] += 1
    max_val = max(counts['values'].values())
    hval = []
    for value, count in counts['values'].items():
        if count == max_val:
            hval.append(value)
    try:
        max_suit = max(counts['suits'].values())
    except ValueError:
        max_suit = None

    # determine best phase play style given hand composition
    if max_val > 3 and phases[2] is False:
        phase = 3
    elif max_val > 3 and phases[4] is False:
        phase = 5
    elif max_val > 2 and len(hval) > 1 and phases[0] is False:
        phase = 1
    elif max_suit is not None and max_suit > 4 and phases[1] is False:
        phase = 2
    elif phases[3] is False:
        phase = 4
    else:
        for status in range(5):
            if phases[status] is False:
                phase = status - 1
                break

    # run for phase yet to be played, else run for phase played
    if played is None:
        discard = gen_discard(phase, player, table, counts)
        viable = gen_viable(phase, player, table, counts)
    else:
        discard = gen_discard(None, player, table, counts)
        viable = gen_viable(None, player, table, counts)
    return discard, viable


def gen_hold(phase, player, table, counts):
    """Generate cards to hold."""
    # initialise collectors and determine hand composition
    max_val = max(counts['values'].values())
    v = counts['values']
    hval = []
    suit = []
    holding = ['ZZ']
    try:
        max_suit = max(counts['suits'].values())
    except ValueError:
        max_suit = None
    for value, count in counts['values'].items():
        if count == max_val:
            hval.append(value)
    for value, count in counts['suits'].items():
        if count == max_suit:
            suit.append(value)

    # always hold largest multiple
    if phase == 1 or phase == 3:
        for card in player.hand:
            if card.value in hval:
                holding.append(card.name)

    # always hold largest suit
    elif phase == 2:
        for card in player.hand:
            if card.suit in suit:
                holding.append(card.name)

    # always hold adjacent cards
    elif phase == 4:
        for card in player.hand:
            pos = card.value
            if v[max((pos - 1), 2)] > 0 or v[min((pos + 1), 13)] > 0:
                if not v[pos] > 1:
                    holding.append(card.name)

    # always hold (part of) largest run and largest multiple value set
    elif phase == 5:
        # split hand into colours
        unique_cards = ([], [])
        card_vals = ([], [])
        values = (dd(int), dd(int))
        for card in player.hand:
            if not card.value >= 20:
                values[card.colour][card.value] += 1
                if card.value not in card_vals[card.colour]:
                    unique_cards[card.colour].append(card.name)
                    card_vals[card.colour].append(card.value)
            # hold largest multiple value set
            if card.value in hval:
                holding.append(card.name)

        # hold (part of) largest run
        longest = longest_run(player)
        max_length = max(longest[0])
        if max_length >= 3:
            for i in range(2):
                if longest[0][i] == max_length:
                    holding += longest[1][i][:4]
        else:
            for colour in longest[1]:
                holding += colour[:4]

    return holding


def gen_viable(phase, player, table, counts):
    """Generate viable cards given hand and table status."""
    v = counts['values']
    discard = table.discard
    viable = []
    if discard is None or discard.name == 'ZZ':
        return viable
    # get discard, try placing on phases
    if phase is None:
        card = [discard]
        logical_plays = []
        valid_plays = []
        gen_4s(card, table, logical_plays)
        check_4s(table, logical_plays, valid_plays)
        # draw from discard if valid play 4
        if len(valid_plays):
            viable.append(discard.name)
            logical_plays.clear()
            valid_plays.clear()
        return viable

    # draw card if at least 2, at most 5 of the same value
    if phase == 1 or phase == 3:
        if 2 <= counts['values'][discard.value] <= 5:
            viable.append(discard.name)

    # draw card if at least 4 of the same suit
    elif phase == 2:
        if counts['suits'][discard.suit] >= 4:
            viable.append(discard.name)

    # draw card if neighbour to held card value and not repeat
    elif phase == 4:
        pos = discard.value
        if v[max((pos - 1), 2)] == 0 or v[min((pos + 1), 13)] == 0:
            if v[pos] == 0:
                viable.append(discard.name)

    # draw card if at least 2 of the same value
    # or neighbour to held card value
    elif phase == 5:
        pos = discard.value
        longest = longest_run(player)
        values = (dd(int), dd(int))
        hval = []
        max_val = max(v.values())
        for value, count in v.items():
            if count == max_val:
                hval.append(value)
        # count by colour
        for card in player.hand:
            if not card.value == 25:
                if not card.colour:
                    values[0][card.value] += 1
                else:
                    values[1][card.value] += 1
        if discard.value in hval and 2 <= v[discard.value] <= 5:
            viable.append(discard.name)

        # both colours same run length
        if len(longest[2]) == 2:
            pass
        # black longest run
        elif not longest[2][0]:
            terminals = (Card(longest[1][0][0]), Card(longest[1][0][-1]))
            if not discard.colour:
                if (discard.value + 1 == terminals[0].value or
                        discard.value - 1 == terminals[1].value):
                    viable.append(discard.name)
        # red longest run
        else:
            terminals = (Card(longest[1][1][0]), Card(longest[1][1][-1]))
            if discard.colour:
                if (discard.value + 1 == terminals[0].value or
                        discard.value - 1 == terminals[1].value):
                    viable.append(discard.name)

        # catch values at edge of values, or middle (joining) card
        pos = discard.value
        col = discard.colour
        start = max((pos - 1), 2)
        end = min((pos + 1), 13)
        if discard.value == 2 or discard.value == 13:
            if values[col][start] > 0 or values[col][end] > 0:
                viable.append(discard.name)
        elif values[col][start] > 0 and values[col][end] > 0:
            viable.append(discard.name)

    return viable


def gen_discard(phase, player, table, counts):
    """Generate discards given hand and table status."""
    # initialise collectors
    discard = []
    natural = []
    wild = []
    mval = []
    hval = []
    suit = []
    hold_4s = []

    # get current conditions for values and suits
    exwild = [card.name for card in player.hand if not card.value >= 20]
    # value conditions
    v = counts['values']
    max_val = max(v.values())
    try:
        min_val = min(v.values())
    except ValueError:
        min_val = None
    for value, count in v.items():
        if count == min_val:
            mval.append(value)
        elif count == max_val:
            hval.append(value)
    # suit conditions
    try:
        min_suit = min(counts['suits'].values())
    except ValueError:
        min_suit = None
    for value, count in counts['suits'].items():
        if count == min_suit:
            suit.append(value)

    # get current draw probabilities and additional hold logic
    prob = prob_count(player, table)
    hold = gen_hold(phase, player, table, counts)

    # do not discard valid plays to next player
    player_phase = table.status[player.pid].phase
    if player.pid + 1 == 4:
        next_player_phase = table.status[0].phase
    else:
        next_player_phase = table.status[player.pid + 1].phase
    if (player_phase is None and next_player_phase is not None):
        test_4s = []
        val_4s = []
        gen_4s(player.hand, table, test_4s)
        check_4s(table, test_4s, val_4s)
        hold_4s = [play[1][0] for play in val_4s]

    # skip player with phase played and skip status unset
    if 'ZZ' in player.hand_list:
        for i in range(4):
            if (not i == player.pid and table.status[i].phase and not
                    prob[4][i]):
                return ['ZZ', i]

    for card in player.hand:
        if card.value == 25:
            wild.append(card)
        else:
            natural.append(card)

    # discard largest value for phase played
    if phase is None:
        for card in natural:
            discard.append(card.name)
        temp = [Card(i) for i in discard]
        temp.sort(key=attrgetter('value'), reverse=True)
        discard = [card.name for card in temp]
        return discard

    if phase == 1 or phase == 3:
        for card in natural:
            # discard lowest (non)multiple
            if card.value in mval:
                discard.append(card.name)
            # discard overdrawn card (essentially 0 probability)
            elif ((prob[2][card.value] <= 0 and card.value not in hval) or
                    card.value not in hval):
                discard.append(card.name)

    elif phase == 2:
        for card in natural:
            # discard smallest suit
            if card.suit in suit:
                discard.append(card.name)
        # sort by highest value
        temp = [Card(i) for i in discard]
        temp.sort(key=attrgetter('value'), reverse=True)
        discard = [card.name for card in temp]
        # for same length suits, hold more probable
        sorting = [(prob[1][Card(i).suit], Card(i)) for i in discard]
        sorting.sort(key=lambda x: x[0])
        discard = [card[1].name for card in sorting]

    elif phase == 4:
        # discard duplicates
        for card in natural:
            if v[card.value] > 1:
                discard.append(card.name)
        # sort by highest value
        temp = [Card(i) for i in discard]
        temp.sort(key=attrgetter('value'), reverse=True)
        discard = [card.name for card in temp]

    elif phase == 5:
        # utilised hold logic for discard
        for card in natural:
            if card.name not in hold:
                if card.value not in hval:
                    discard.append(card.name)
        if not len(discard):
            for card in natural:
                if card.value in hval:
                    discard.append(card.name)

    # sort by highest value, then by probability (hold more probable)
    if phase == 1 or phase == 3 or phase == 5:
        temp = [Card(i) for i in discard]
        temp.sort(key=attrgetter('value'), reverse=True)
        discard = [card.name for card in temp]
        sorting = [(prob[2][Card(i).value], Card(i)) for i in discard]
        sorting.sort(key=lambda x: x[0])
        discard = [card[1].name for card in sorting]

    # clear cards not caught by basic logic
    for card in hold:
        if card in discard:
            discard.remove(card)
    for card in hold_4s:
        if card in discard:
            discard.remove(card)
    if not len(discard):
        discard.append(exwild[-1])

    return discard


def phasedout_bonus(player_id, table, turn_history, phase_status, hand,
                    discard):
    """phasedout_bonus returns the best move given the game status."""
    # get current game status
    player = Player(player_id, phase_status[player_id], hand)
    table = Table(table, turn_history, phase_status, discard)
    curr_phase = table.status[player_id].phase
    try:
        last_move = table.history[-1][-1][-1][0]
    except IndexError:
        last_move = 0

    analysis = card_count(player, table)
    best_discard, viable = analysis[0], analysis[1]
    if last_move == 0 or last_move >= 5:
        if table.discard.name in viable:
            return (2, table.discard.name)
        else:
            return (1, None)

    # try move 3
    if (last_move == 1 or last_move == 2) and curr_phase is None:
        return phase_play(player, table, best_discard)

    # phase has been played, try move 4
    elif curr_phase is not None:
        return valid_4s(player, table, best_discard)


if __name__ == '__main__':
    # Example call to the function.
    print(phasedout_bonus(0,
                          [(None, []), (None, []), (None, []), (None, [])],
                          [(0, [(2, 'JS')])],
                          [(False, False, False, False, False),
                              (False, False, False, False, False),
                              (False, False, False, False, False),
                              (False, False, False, False, False)],
                          ['5D', '3H', '0C', '2H',
                              '2C', '7H', 'KS', 'AS', 'ZZ', 'JC'],
                          'ZZ')
          )
