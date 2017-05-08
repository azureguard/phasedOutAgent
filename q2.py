"""Project 3 Q2."""
from classes import Set


def phasedout_phase_type(phase):
    """phasedout_phase_type returns the phase type of a list of cards."""
    num_groups = len(phase) - 1
    if num_groups:
        return Set(phase[0], phase[1]).phase
    else:
        return Set(phase[0]).phase


if __name__ == '__main__':
    # Example calls to the function.
    print(phasedout_phase_type([['2C', '2S', '2H'], ['7H', '7C', 'AH']]))
    print(phasedout_phase_type([['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']]))
    print(phasedout_phase_type(
        [['4H', '4S', 'AC', '4C'], ['7H', '7C', 'AH', 'AC']]))
    print(phasedout_phase_type(
        [['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']]))
    print(phasedout_phase_type(
        [['4H', '5D', 'AC', '7H'], ['7H', '7C', 'AH', 'AS']]))
    print(phasedout_phase_type([['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']]))
