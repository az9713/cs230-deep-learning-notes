"""Original finite-model checks; no neural training or career prediction."""
import math


def chance_of_success(probability, attempts, shared_fraction=0.0):
    """Equal marginals; mixture of independent trials and one shared outcome."""
    if (not isinstance(attempts, int) or isinstance(attempts, bool)
            or attempts < 0):
        raise ValueError('attempts must be a nonnegative integer')
    for value in (probability, shared_fraction):
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError('probabilities must be finite numbers')
        if not 0 <= value <= 1:
            raise ValueError('probabilities must be in [0, 1]')
    if attempts == 0 or probability == 0:
        return 0.0
    independent = (1.0 if probability == 1 else
                   -math.expm1(attempts * math.log1p(-probability)))
    return ((1 - shared_fraction) * independent
            + shared_fraction * probability)


def precision(prevalence, sensitivity, false_positive_rate):
    """Bayes' rule for a binary detector; undefined if no positive calls."""
    values = (prevalence, sensitivity, false_positive_rate)
    if any(not isinstance(v, (int, float)) or not math.isfinite(v)
           or not 0 <= v <= 1 for v in values):
        raise ValueError('rates must be finite numbers in [0, 1]')
    true_positive = prevalence * sensitivity
    false_positive = (1 - prevalence) * false_positive_rate
    denominator = true_positive + false_positive
    return true_positive / denominator if denominator else None


def self_check():
    assert math.isclose(chance_of_success(0.1, 20), 1 - 0.9 ** 20)
    assert chance_of_success(0.1, 20, 1) == 0.1
    assert math.isclose(chance_of_success(0.1, 20, 0.5),
                        (1 - 0.9 ** 20 + 0.1) / 2)
    assert chance_of_success(1, 0, 1) == 0
    assert chance_of_success(1, 2) == 1
    assert chance_of_success(0, 200) == 0
    assert chance_of_success(1e-20, 1) > 0
    assert math.isclose(precision(0.01, 0.9, 0.05), 0.009 / 0.0585)
    assert precision(0.5, 1, 0) == 1
    assert precision(0.5, 0, 0) is None
    for args in ((-0.1, 2), (0.1, -1), (0.1, 2.5),
                 (float('nan'), 2), (0.1, 2, 1.1)):
        try:
            chance_of_success(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(f'invalid domain accepted: {args}')
    try:
        precision(0.1, float('inf'), 0.2)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid detector rate accepted')
    print('Portfolio and detector checks passed.')
    print(f'20 independent attempts, p=0.1: {chance_of_success(0.1, 20):.6f}')
    print(f'20 shared-outcome attempts, p=0.1: {chance_of_success(0.1, 20, 1):.6f}')
    print(f'Precision at 1% prevalence: {precision(0.01, 0.9, 0.05):.6f}')


if __name__ == '__main__':
    self_check()
