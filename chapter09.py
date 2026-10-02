"""Chapter 9 original numerical fixtures. Run with Python 3; standard library only."""
import math


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def matvec(matrix, x):
    return [dot(row, x) for row in matrix]


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def close(actual, expected, tol=1e-10):
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        actual, expected)


def dog_probability(x):
    # Stable two-class softmax for logits x[0] and 2*x[1].
    margin = x[0] - 2 * x[1]
    return 1 / (1 + math.exp(-margin))


def relu_score(x):
    return max(0, 2*x[0]-x[1]-1) + 0.5*max(0, x[1])


def relu_gradient(x):
    active = float(2*x[0]-x[1]-1 > 0)
    return [2*active, -active + 0.5*float(x[1] > 0)]


def integrated_gradients(score_gradient, x, baseline, intervals):
    # Right-endpoint rectangle rule, not exact integration.
    displacement = [a-b for a, b in zip(x, baseline)]
    sums = [0.0]*len(x)
    for step in range(1, intervals+1):
        fraction = step/intervals
        point = [b+fraction*d for b, d in zip(baseline, displacement)]
        for i, value in enumerate(score_gradient(point)):
            sums[i] += value
    return [d*s/intervals for d, s in zip(displacement, sums)]


def conv_matrix():
    # Five outputs, eight genuine inputs, two fixed padding zeros per side.
    return [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, -1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, -1, 0],
    ]


def full_convolution(x, kernel):
    result = [0.0]*(len(x)+len(kernel)-1)
    for i, value in enumerate(x):
        for j, weight in enumerate(kernel):
            result[i+j] += value*weight
    return result


def pooled_and_unpooled(window):
    maximum = max(window)
    switch = window.index(maximum)  # deterministic first-maximum convention
    unpooled = [0.0]*len(window)
    unpooled[switch] = maximum
    return maximum, unpooled


def word_ngrams(text, length):
    words = text.lower().split()  # This fixture deliberately keeps punctuation.
    return {tuple(words[i:i+length]) for i in range(len(words)-length+1)}


def run():
    # Probability can change even though the dog logit stays fixed.
    before, after = dog_probability([1, 1]), dog_probability([1, 0])
    close(before, 0.2689414213699951)
    close(after, 0.7310585786300049)
    step = 1e-6
    derivative = (dog_probability([1, 1+step])
                  - dog_probability([1, 1-step]))/(2*step)
    close(derivative, -2*before*(1-before), 1e-8)
    print("softmax:", round(before, 6), "->", round(after, 6))

    # A path crosses one kink at fraction 1/3.
    x, baseline = [2, 1], [0, 0]
    exact = [8/3, -1/6]
    approx = integrated_gradients(relu_gradient, x, baseline, 3000)
    for actual, expected in zip(approx, exact):
        close(actual, expected)
    close(sum(approx), relu_score(x)-relu_score(baseline))
    assert dot(relu_gradient(x), x) == 3.5
    # Deliberately coarse quadrature is detected by a completeness residual.
    coarse = integrated_gradients(relu_gradient, x, baseline, 2)
    assert abs(sum(coarse)-relu_score(x)) > 0.1
    print("IG:", [round(value, 6) for value in approx],
          "sum", round(sum(approx), 6))

    # Ordinary finite differences validate the adjoint/chain-rule calculation.
    matrix = conv_matrix()
    original = list(range(1, 9))
    output = matvec(matrix, original)
    assert output == [2, 3, 3, 3, -7]
    signal = [0.3, -0.7, 1.1, 0.9, -0.2]
    adjoint = matvec(transpose(matrix), signal)
    close(dot(output, signal), dot(original, adjoint))
    for i, expected in enumerate(adjoint):
        plus, minus = original[:], original[:]
        plus[i] += step
        minus[i] -= step
        observed = (dot(matvec(matrix, plus), signal)
                    - dot(matvec(matrix, minus), signal))/(2*step)
        close(observed, expected, 1e-8)
    gram = [[dot(row, other) for other in matrix] for row in matrix]
    assert gram == [[1, 0, 0, 0, 0], [0, 2, 0, 0, 0],
                    [0, 0, 2, 0, 0], [0, 0, 0, 2, 0],
                    [0, 0, 0, 0, 1]]
    scaled = [u/d for u, d in zip(output, [1, 2, 2, 2, 1])]
    minimum_norm = matvec(transpose(matrix), scaled)
    assert matvec(matrix, minimum_norm) == output
    assert minimum_norm != original
    null_direction = [1, 0, 0, 1, 0, 0, 0, 0]
    assert matvec(matrix, null_direction) == [0]*5
    close(dot(minimum_norm, null_direction), 0)
    incorrectly_halved = [a/2 for a in matvec(transpose(matrix), output)]
    assert matvec(matrix, incorrectly_halved) != output
    zero_inserted = [value for u in signal for value in (u, 0)][:-1]
    cropped = full_convolution(zero_inserted, [-1, 0, 0, 1])[2:-2]
    for actual, expected in zip(cropped, adjoint):
        close(actual, expected)
    print("transpose:", output, "minimum-norm preimage:", minimum_norm)

    # Mean-pooling CAM identity, including bias and Grad-CAM scale.
    maps, weights, bias = [[1, 2, 3, 4], [4, 3, 2, 1]], [2, -1], 0.5
    pooled = [sum(values)/4 for values in maps]
    logit = dot(weights, pooled)+bias
    cam = [dot(weights, pixel) for pixel in zip(*maps)]
    assert cam == [-2, 1, 4, 7]
    close(logit, sum(cam)/4+bias)
    gradcam_weights = [weight/4 for weight in weights]
    raw_gradcam = [dot(gradcam_weights, pixel) for pixel in zip(*maps)]
    for actual, expected in zip(raw_gradcam, cam):
        close(actual, expected/4)
    orange = [44, 94, 42, 22, 123, 231, 83, 2,
              34, 255, 232, 92, 34, 76, 187, 124]
    close(sum(orange)/16, 104.6875)
    print("CAM:", cam, "logit:", logit)

    # Zero-filled unpool is a right inverse only with the stated conditions.
    positive, restored = pooled_and_unpooled([1, 6, 2, 4])
    assert max(restored) == positive
    negative, restored = pooled_and_unpooled([-4, -3, -2, -1])
    assert negative == -1 and max(restored) == 0
    rules = []
    for preactivation, incoming in [(2, 3), (2, -3), (-2, 3), (-2, -3)]:
        rules.append((incoming*int(preactivation > 0),
                      incoming*int(incoming > 0),
                      incoming*int(preactivation > 0)*int(incoming > 0)))
    assert rules == [(3, 3, 3), (-3, 0, 0), (0, 3, 0), (0, 0, 0)]

    # Same attention output despite different routing distributions.
    close(dot([0.9, 0.1], [2, 2]), dot([0.1, 0.9], [2, 2]))
    old_loss, new_loss = dot([0.5, 0.5], [1, 2]), dot([0.25, 0.75], [1, 2])
    close(new_loss-old_loss, 0.25)
    train_grams = word_ngrams("the dog sees the fence", 2)
    test_cases = ["the dog runs", "cat sleeps"]
    test_sets = [word_ngrams(case, 2) for case in test_cases]
    all_test_grams = set().union(*test_sets)
    close(len(train_grams & all_test_grams)/len(all_test_grams), 1/3)
    close(sum(bool(train_grams & grams) for grams in test_sets)/len(test_sets), 1/2)
    # Paired binary capability comparison: 4 wins, 1 loss, 5 ties.
    differences = [1]*4 + [-1] + [0]*5
    mean = sum(differences)/len(differences)
    variance = sum((d-mean)**2 for d in differences)/(len(differences)-1)
    close(mean, 0.3)
    close(math.sqrt(variance/len(differences)), math.sqrt(4.1/90))
    # Equal scaling exponents imply balanced sqrt allocation.
    compute = 600
    n_param = math.sqrt(compute/6)
    n_tok = compute/(6*n_param)
    close(n_param, 10)
    close(n_tok, 10)
    risk = lambda n: 1/n + 1/(compute/(6*n))
    assert risk(n_param) < risk(5) and risk(n_param) < risk(20)
    print("mixture:", old_loss, "->", new_loss,
          "paired gain:", mean, "SE:", round(math.sqrt(variance/10), 6))
    print("All chapter 9 numerical checks passed.")


if __name__ == "__main__":
    run()
