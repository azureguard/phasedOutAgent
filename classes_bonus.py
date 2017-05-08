"""Project 3 Classes."""
from operator import attrgetter


class Card():
    """Definition of card with value, suit, colour and name."""

    # constants used for card definition
    COLOUR = {'C': 0, 'D': 1, 'H': 1, 'S': 0, 'Z': 2}
    VAL = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '0': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 25,
        'Z': 20
    }

    def __init__(self, card):
        """Initialise card with values mapped to constants."""
        self.value = self.VAL[str(card[0])]
        self.suit = card[1]
        self.colour = self.COLOUR[card[1]]
        self.name = card


class Group():
    """Definition of a group of cards."""

    def __init__(self, cards, curr_group=None):
        """Initialise group with list of cards and set group type."""
        self.cards = [Card(i) for i in cards]
        self.score = sum([card.value for card in self.cards])
        # set current group from basic definitions else set to given group
        if curr_group is None:
            self.group = self.set_group()
        else:
            self.group = curr_group

    def add_card(self, card, pos):
        """Add card to group, given valid position."""
        # attempted position is beyond length of list
        if pos > len(self.cards):
            return False
        self.cards.insert(pos, Card(card))
        return True

    def check_run(self, check_val):
        """Check run order of given group."""
        # get value and position of first natural card
        check = min(check_val) - check_val.index(min(check_val))
        if check < 2:
            return False
        for val in check_val:
            # increment counter by 1 on wild
            if val == 25:
                check += 1
            # run broken
            elif not val == check:
                return False
            else:
                check += 1
                # run out of bounds
        if check > 14:
            return False
        return len(self.cards)

    def check_add(self, pos, card, curr_group):
        """Check validity of addition to group."""
        # try positional addition first
        if self.add_card(card, pos) is False:
            return False
        # define check variables
        wild = 0
        natural = 0
        check_val = []
        check_suit = []
        check_col = []

        # determine composition of cards
        for i in self.cards:
            # exclude wild cards from suit and colour count
            if not i.value == 25:
                natural += 1
                check_suit.append(i.suit)
                check_col.append(i.colour)
            else:
                wild += 1
            # wild inluded to determine position of wild within runnning order
            check_val.append(i.value)

        # recheck group from base definitions
        # sets used to determine number of values, suits and colours
        # group type 1 or 3
        if curr_group == 1 or curr_group == 3:
            # no wild card
            if len(set(check_val)) == 1:
                return True
            # with wild card(s)
            if len(set(check_val)) == 2 and wild > 0:
                return True

        # group type 2
        elif curr_group == 2 and len(set(check_suit)) == 1:
            return True

        # group type 4 or 5
        elif curr_group >= 4:
            # wrong colour added
            if curr_group == 5 and not len(set(check_col)) == 1:
                return False
            return self.check_run(check_val)

        return False

    def set_group(self):
        """Check group type using base definitions."""
        # define check variables
        natural = 0
        length = len(self.cards)
        check_val = []
        check_suit = []
        check_col = []

        # determine composition of cards
        for i in self.cards:
            # exclude wild cards from suit and colour count
            if not i.value == 25:
                natural += 1
                check_suit.append(i.suit)
                check_col.append(i.colour)
            # wild included to determine position of wild within runnning order
            check_val.append(i.value)

        # start of base definition check of group type
        # sets used to determine number of values, suits and colours
        if natural >= 2:
            # group type 1 no wild card
            # group type 1 with wild card
            if ((length == 3 and len(set(check_val)) == 1) or
                (length == 3 and len(set(check_val)) == 2 and natural < 3 and
                 25 in check_val)):
                return 1

            # group type 2
            if length == 7 and len(set(check_suit)) == 1:
                return 2

            # group type 3 no wild card or
            # group type 3 with wild card(s)
            if ((length == 4 and len(set(check_val)) == 1) or
                (length == 4 and len(set(check_val)) == 2 and
                 25 in check_val)):
                return 3

            # group type 4
            if length == 8 and self.check_run(check_val):
                return 4

            # group type 5
            if (length == 4 and len(set(check_col)) == 1 and
                    self.check_run(check_val)):
                return 5

        return None


class Set():
    """Definition of a set with phase determined by group composition."""

    def __init__(self, g1=[], g2=[], phase_status=None):
        """Initialise set given groups, phase_status."""
        # create set given pre-checked validity (set on table)
        if phase_status is not None:
            self.g1_stat, self.g2_stat = self.get_group(phase_status)
            self.group = ((Group(g1, self.g1_stat), Group(g2, self.g2_stat)))
            self.phase = phase_status
        # create set fresh (attempt play)
        else:
            self.group = ((Group(g1), Group(g2)))
            self.phase = self.set_phase()
        self.cards = self.group[0].cards + self.group[1].cards
        self.score = sum(
            [card.value for card in self.cards if not card.value == 25])

    def get_group(self, phase):
        """Determine group composition for valid set."""
        if phase == 1:
            return (1, 1)
        if phase == 2:
            return (2, None)
        if phase == 3:
            return (3, 3)
        if phase == 4:
            return (4, None)
        if phase == 5:
            return (5, 3)

    def set_phase(self):
        """Determine phase type from group composition of fresh set."""
        groups = (self.group[0].group, self.group[1].group)
        if groups[0] == 1 and groups[1] == 1:
            return 1
        if groups[0] == 2 and groups[1] is None:
            return 2
        if groups[0] == 3 and groups[1] == 3:
            return 3
        if groups[0] == 4 and groups[1] is None:
            return 4
        if groups[0] == 5 and groups[1] == 3:
            return 5
        return None


class Player():
    """Definition of a player with player id, phase_status and hand."""

    def __init__(self, pid, phase_status, hand):
        """Initialise player."""
        self.pid = pid
        self.phase = phase_status
        self.hand = [Card(i) for i in hand]
        self.sort_hand()
        self.hand_list = [card.name for card in self.hand]
        self.score = sum([card.value for card in self.hand])

    def sort_hand(self):
        """Sort player hand by value."""
        self.hand = sorted(self.hand, key=attrgetter('value'))

    def discard(self, remove):
        """Check validity of play from player hand."""
        for card in remove:
            success = False
            for holding in self.hand:
                if card == holding.name:
                    self.hand.remove(holding)
                    success = True
                    break
            if not success:
                return False
        return True


class Table():
    """Definition of table with current game status."""

    def __init__(self, table, turn_history, phase_status, discard):
        """Initialise table from status given."""
        self.status = []
        # create sets for each player
        for i in table:
            if len(i[1]) == 0:
                self.status.append(Set(phase_status=i[0]))
            if len(i[1]) == 1:
                self.status.append(Set(i[1][0], phase_status=i[0]))
            if len(i[1]) == 2:
                self.status.append(Set(i[1][0], i[1][1], phase_status=i[0]))
        self.history = turn_history
        self.phase_status = phase_status
        # create discard pile (top card)
        try:
            self.discard = Card(discard)
        except TypeError:
            self.discard = None

    def check_play(self, play, player):
        """Determine if play is valid."""
        # get previous player move, if error, first move of game
        try:
            prev_move = self.history[-1][-1][-1][0]
        except IndexError:
            prev_move = 0
        # get current player move
        curr_move = play[0]

        # rule check for valid move
        if (1 <= curr_move <= 2 and not prev_move == 0 or
                curr_move == 3 and not 1 <= prev_move <= 3 or
                curr_move == 4 and not 1 <= prev_move <= 3 or
                curr_move == 5 and (prev_move == 0 or prev_move == 5)):
            return False

        # check for validity of attempted phase play
        if curr_move == 3:
            if len(play[1]) > 1:
                # check if player is holding requisite cards
                play_valid = player.discard(play[1][0] + play[1][1])
                # get phase of played set
                phase_check = Set(play[1][0], play[1][1]).phase
            else:
                # check if player is holding requisite cards
                play_valid = player.discard(play[1][0])
                # get phase of played set
                phase_check = Set(play[1][0]).phase

            # requisite cards not held or
            # attempted play does not form a phase or
            # player attempted play of played phase
            if (not play_valid or phase_check is None or
                    self.phase_status[player.pid][phase_check]):
                return False
            else:
                return True

        # check for validity of attempted play onto set on table
        if curr_move == 4:
            # player has not played a phase in current round or
            # player is not holding requisite cards
            if (self.status[player.pid].phase is None or
                    not player.discard([play[1][0]])):
                return False
            # get card, player set and group, and position of attempted play
            c_add = play[1][0]
            p_mod = play[1][1][0]
            g_mod = self.status[p_mod].group[play[1][1][1]]
            curr_group = g_mod.group
            index_mod = play[1][1][2]
            # check validity of addition to group
            if g_mod.check_add(index_mod, c_add, curr_group):
                return True
            else:
                return False

        # check if card in player hand for discard
        if curr_move == 5:
            return player.discard([play[1]])
