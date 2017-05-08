# comp10001-project3

Project 3 of COMP10001 (2017s1)

## Phased Out

Implements functionality and rudimentary AI to play a card game.

## [q1](q1.py)

Write a function called phasedout_group_type that takes the following single
argument:

### group

A group of cards in the form of a list, each element of which is a 2-character
string with the value (drawn from '234567890JQKA') followed by the suit (drawn
from 'SHDC'), e.g. ['2C', '2S', '2H'] represents a group of three cards, made up
of the Two of Clubs, the Two of Spades, and the Two of Hearts.

The function should return one of the following values, indicating the type of
group of cards contained in group:

1: A set of three cards of the same value, e.g. ['2C', '2S', '2H'] represents a
set of three Twos. Note that the set may include Wilds, but must include at
least two "natural" cards (i.e. non-Wild cards), which define the value. Note
also that the sequence of the cards is not significant for this group type.

2: A set of 7 cards of the same suit, e.g. ['2C', '2C', '4C', 'KC', '9C', 'AH',
'JC'] represents a set of seven Clubs. Note that the set may include Wilds (as
we see in our example, with the Ace of Hearts), but must include at least two
"natural" cards (i.e. non-Wild card), which define the suit. Note also that the
sequence of the cards is not significant for this group type.

3: A set of four cards of the same value, e.g. ['4H', '4S', 'AC', '4C']
represents a set of four Fours. Note that the set may include Wilds (as we see
in our example, with the Ace of Clubs), but must include at least two "natural"
cards (i.e. non-Wild cards), which define the value. Note also that the sequence
of the cards is not significant for this group type.

4: A run of eight cards, e.g. ['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']
represents a run of eight cards. Note that the set may include Wilds (as we see
in our example, with the Ace of Clubs standing in for a Six and the Ace of
Hearts standing in for a Nine), but must include at least two "natural" cards
(i.e. non-Wild cards). Note also that the sequence of the cards is significant
for this group type, and that ['4H', '5S', 'AC', '8H', '7C', 'AH', '0S', 'JC'],
e.g., is not a valid run of eight, as it is not in sequence.

5: A run of four cards of the same colour, e.g. ['4H', '5D', 'AC', '7H']
represents a run of four Red cards. Note that the set may include Wilds (as we
see in our example, with the Ace of Clubs standing in for a Red Six), but must
include at least two "natural" cards (i.e. non-Wild cards), which define the
colour. Note also that the sequence of the cards is significant for this group
type, and that ['4H', '5D', '7H', 'AC'] is not a valid run of four cards of the
same colour, as it is not in sequence.

None: Any combination of cards which does not correspond to one of the above
group types (e.g. ['4H', '5D', '7C', 'AC'].

## [q2](q2.py)

Write a function called phasedout_phase_type that takes the following single
argument:

### phase

A combination of card groups in the form of a list of lists of cards, where each
card is a 2-character string with the value (drawn from '234567890JQKA')
followed by the suit (drawn from 'SHDC'), e.g. [['2C', '2S', '2H'], ['7H', '7C',
'AH']] represents an instance of two sets of three cards of the same value, as
it is made up of two groups, each of which is a set of three cards of the same
value. The function should return one of the following values, indicating the
type of the combination of card groups contained in phase:

1: Two sets of three cards of the same value, e.g. [['2C', '2S', '2H'], ['7H',
'7C', AH']] represents a set of three Twos and three Sevens. Note that each set
may include Wilds (as we see in our example, with the Ace of Hearts), but must
include at least two "natural" cards (i.e. non-Wild cards), which define the
value.

2: One set of 7 cards of the same suit, e.g. [['2C', '2C', '4C', 'KC', '9C',
'AH', 'JC']] represents a single set of seven Clubs. Note that the set may
include Wilds (as we see in our example, with the Ace of Hearts), but must
include at least two "natural" cards (i.e. non-Wild cards), which define the
suit.

3: Two sets of four cards of the same value, e.g. [['4H', '4S', 'AC', '4C'],
['7H', '7C', 'AH', 'AC']] represents a set of four Fours and a set of four
Sevens. Note that each set may include Wilds (as we see in our example, with the
two Aces of Clubs and Ace of Hearts), but must include at least two "natural"
cards (i.e. non-Wild cards), which define the value.

4: One run of eight cards, e.g. [['4H', '5S', 'AC', '7C', '8H', 'AH', '0S',
'JC']] represents a single run of eight cards. Note that the set may include
Wilds (as we see in our example, with the Ace of Clubs standing in for a Six and
the Ace of Hearts standing in for a Nine), but must include at least two
"natural" cards (i.e. non-Wild cards). Note also that the sequence of the cards
is significant for this group type, and that [['4H', '5S', 'AC', '8H', '7C',
'AH', '0S', 'JC']], e.g., is not a valid instance of this phase type, as the run
is not in sequence.

5: A run of four cards of the same colour and a set of four cards of the same
value, e.g. [['4H', '5D', 'AC', '7H'], ['7H', '7C', 'AH', 'AS']] represents a
run of four Red cards and a set of four Sevens. Note that each set may include
Wilds (as we see in our example, with the Ace of Clubs standing in for a Red
Six, and Ace of Hearts and Ace of Spaces standing in for Sevens), but must
include at least two "natural" cards (i.e. non-Wild cards), which define the
colour/value. Note also that the sequence of the cards within the run is
significant for this group type, and also that the sequence of the two groups is
significant, in that the run must come before the set of four.

None: Any combination of groups of cards which does not correspond to one of the
above phase types (e.g. [['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']].

## [q3](q3.py)

Write a function called phasedout_is_valid_play that takes the following
arguments:

### play

A 2-tuple indicating the play type, and the content of the play, as follows:

1: Pick up a card from the top of the deck at the start of the player's turn,
with the play content being the card that was picked up (e.g. (1, 'JS')).

2: Pick up a card from the top of the discard pile at the start of the player's
turn, with the play content being the card that was picked up (e.g. (2, '2C')).

3: Place a phase to the table from the player's hand, with the play content
being the phase (e.g. (3, [['2S', '2S', '2C'], ['AS', '5S', '5S']])).

4: Place a single card from the player's hand to a phase on the table, with the
play content being a 2-tuple made up of the card the player is attempting to
play, and the position they are attempting to play it in, itself in the form of
a 3-tuple indicating: (1) the player ID of the phase the card is to be placed
on; (2) the group within the phase the card is to placed in; and (3) the index
of the position within the group the card is to be played to. For example, (4,
('AD', (1, 0, 3))) indicates that an Ace of Diamonds is to be placed on the
phase of Player 1, in Group 1 and index position 3 (i.e. it will be the fourth
card in Group 1).

5: Discard a single card from the player's hand, and in doing so, end the turn
(e.g. (5, 'JS') indicates that a Jack of Spades is to be discarded).

### player_id

An integer between 0 and 3 inclusive, indicating the ID of the player attempting
the play.

### table

A 4-element list of phase plays for each of Players 0—3, respectively. Each
phase play is in the form of a 2-tuple indicating the phase content (as an
integer or None, consistent with the output of phasedout_phase_type) and a list
of lists of cards (of the same format as for phasedout_phase_type, but possibly
with extra cards played to each of the groups in the phase). An empty phase for
a given player will take the form (None, []). As an example of a full 4-player
table, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S', '5D']]), (None,
[]), (None, [])] indicates that Players 0, 2 and 3 are yet to play a phase for
the hand, and Player 1 has played Phase 1, in the form of a set of Twos and a
set of Fives, the latter of which has had one extra card added to it.

### turn_history

A list of all turns in the game to date, in sequence of play. Each turn takes
the form of a 2-tuple made up of the Player ID and the list if individual plays
in the turn (based on the same format as for play above, with the one difference
that for any draws from the deck, the card is indicated as 'XX' (as it is not
visible to other players). For example, [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2,
'JS'), (3, [['2S', '2S', '2C'], ['AS', '5S', '5S']])])] indicates that the game
to date is made up of two turns, on the part of Players 0 and 1, respectively.
Player 0 first drew the Jack of Spades from the discard pile, then discarded the
Jack of Spades (presumably they had a change of heart!). Player 1 then picked up
the Jack of Spades from the discard pile, and played a phase, in the form of two
sets of three cards of the same value (i.e. Phase 1).

### phase_status

A 4-element indicating the phases that each of Players 0—3, respectively, have
achieved in the game. For example, [0, 4, 0, 0] indicates that Players 0, 2 and
3 have not got any phases, but Player 1 has achieved up to Phase 4. At the start
of a game, this is initialised to [0, 0, 0, 0].

### hand

The list of cards that the current player holds in their hand, each of which is
in the form of a 2-element string.

### discard

The top card of the discard stack, in the form of a 2-element string (e.g.
'3D'). Your function should return True if play is valid relative to the current
game state, and False otherwise.

## [q4](q4.py)

Write a function called phasedout_score that takes the following single argument:

### hand

The list of cards that the current player holds in their hand, each of which is
in the form of a 2-element string.

Your function should return the score for the hand (assuming the game has ended,
and the player is left with the cards in hand) as a non-negative integer.

## [q5](q5.py)

Write a function called phasedout_play that takes the following arguments:

### player_id

An integer between 0 and 3 inclusive, indicating the ID of the player attempting
the play.

### table

A 4-element list of phase plays for each of Players 0—3, respectively. Each
phase play is in the form of a 2-tuple indicating the phase type (as an integer
or None, consistent with the output of phasedout_phase_type) and a list of lists
of cards (of the same format as for phasedout_phase_type, but possibly with
extra cards played to each of the groups in the phase). An empty phase for a
given player will take the form (None, []). As an example of a full 4-player
table, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S', '5D']]), (None,
[]), (None, [])] indicates that Players 0, 2 and 3 are yet to play a phase for
the hand, and Player 1 has played Phase 1, in the form of a set of Twos and a
set of Fives, the latter of which has had one extra card added to it.

### turn_history

A list of all turns in the game to date, in sequence of play. Each turn takes
the form of a 2-tuple made up of the Player ID and the list if individual plays
in the turn (based on the same format as for play above, with the one difference
that for any draws from the deck, the card is indicated as 'XX' (as it is not
visible to other players). For example, [(0, [(1, 'JS'), (5, 'JS')]), (1, [(1,
'JS'), (2, [['2S', '2S', '2C'],['AS', '5S', '5S']])])] indicates that the game
to date is made up of two turns, on the part of Players 0 and 1, respectively.
Player 0 first drew the Jack of Spades from the discard pile, then discarded the
Jack of Spades (presumably they had a change of heart!). Player 1 then picked up
the Jack of Spades from the discard pile, and played a phase, in the form of two
sets of three cards of the same value (i.e. Phase 1).

### phase_status

A 4-element indicating the phases that each of Players 0—3, respectively, have
achieved in the game. For example, [0, 4, 0, 0] indicates that Players 0, 2 and
3 have not got any phases, but Player 1 has achieved up to Phase 4. At the start
of a game, this is initialised to [0, 0, 0, 0].

### hand

The list of cards that the current player holds in their hand, each of which is
in the form of a 2-element string. discard

The top card of the discard stack, in the form of a 2-element string (e.g.
'3D'). Your function should return a 2-tuple describing the single play your
player wishes to make, made up of a play ID and associated play content, as
described below:

1: Pick up a card from the top of the deck at the start of the player's turn. In
this case, the card at the top of the deck is unknown at the time the play is
determined, so the play content is set to None (i.e. (1, None)).

2: Pick up a card from the top of the discard pile at the start of the player's
turn, with the play content taking the value of discard (e.g. (2, '2C')).

3: Place a phase to the table from the player's hand, with the play type being
the phase (e.g. (3, [['2S', '2S', '2C'], ['AS', '5S', '5S']])).

4: Place a single card from the player's hand to a phase on the table, with the
play type being a 2-tuple made up of the card the player is attempting to play,
and the position they are attempting to play it in, itself in the form of a
3-tuple indicating: (1) the player ID of the phase the card is to be placed on;
(2) the group within the phase the card is to placed in; and (3) the index of
the position within the group the card is to be played to. For example, (4,
('AD', (1, 0, 3))) indicates that an Ace of Diamonds is to be placed on the
phase of Player 1, in Group 1 and index position 3 (i.e. it will be the fourth
card in Group 1).

5: Discard a single card from the player's hand, and in doing so, end the turn
(e.g. (5, 'JS') indicates that a Jack of Spades is to be discarded).

## [q6](q6.py)

Functionally the same as q5 but with tweaked rules that allow for adversarial
play with the addition of the Joker card (labelled Z) that when played against
a player, skips their next turn.
