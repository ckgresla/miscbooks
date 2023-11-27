# An example of calculating pass @ the rate k, from the OpenAI Codex Paper- https://arxiv.org/pdf/2107.03374.pdf
import numpy as np

def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$

    + MODEL GENERATED BABY!
    """
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0-k / np.arange(n - c + 1, n + 1))




# res = pass_at_k(123, 43, k=12)
for k in [1, 10, 100]:
    result = pass_at_k(1000, 40, k=k)
    print(f"pass @ {k} = {100*result:.2f}%")
