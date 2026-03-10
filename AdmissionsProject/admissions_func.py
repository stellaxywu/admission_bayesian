import numpy as np
import pandas as pd


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def simulate_admissions(
    df: pd.DataFrame,
    beta0: float,
    beta1: float,
    gamma: float,
    sigma_noise: float,
    seed: int = 0,
) -> pd.DataFrame:
    """
    Admit a fixed-size class under the noisy model:

        P(Y_i=1) = sigma(beta0 + beta1*Q_i + gamma*Z_i + eps_i)
        eps_i ~ N(0, sigma_noise^2)

    sigma_noise represents unobserved holistic factors (essays,
    extracurriculars, interviews) that the model cannot directly observe.

    Class size is fixed to the gamma=0, no-noise expected count so that
    bias shows up as a shift in racial composition, not total class size.
    """
    df  = df.copy()
    rng = np.random.default_rng(seed)
    n   = len(df)
    Q   = df["Q"].values
    Z   = df["Z"].values

    # Fix class size: expected admits under gamma=0, no noise
    p_unbiased = sigmoid(beta0 + beta1 * Q)
    n_target   = p_unbiased.sum()

    # Draw noise
    eps = rng.normal(0, sigma_noise, size=n)

    # Find beta0 adjustment so expected admits equals n_target
    def expected_admits(adj):
        return sigmoid(beta0 + adj + beta1 * Q + gamma * Z + eps).sum()

    lo, hi = -10.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if expected_admits(mid) < n_target:
            lo = mid
        else:
            hi = mid
    adj = (lo + hi) / 2

    p = sigmoid(beta0 + adj + beta1 * Q + gamma * Z + eps)
    df["p"]   = p
    df["eps"] = eps
    df["Y"]   = rng.binomial(1, p)

    return df


def log_likelihood(
    gamma: float,
    df: pd.DataFrame,
    beta0: float,
    beta1: float,
    sigma_noise: float,
    n_samples: int = 50,
    seed: int = 1,
) -> float:
    """
    Marginal log-likelihood integrating out noise:

        log P(D|gamma) = sum_i log E_eps[ p_i(gamma, eps)^Y_i * (1-p_i)^(1-Y_i) ]

    Approximated by Monte Carlo over n_samples noise draws per applicant.
    """
    rng = np.random.default_rng(seed)
    Q   = df["Q"].values
    Z   = df["Z"].values
    Y   = df["Y"].values
    n   = len(df)

    # eps shape: (n_samples, n)
    eps = rng.normal(0, sigma_noise, size=(n_samples, n))
    logits = beta0 + beta1 * Q[None, :] + gamma * Z[None, :] + eps
    p = np.clip(sigmoid(logits), 1e-12, 1 - 1e-12)

    # likelihood per sample per applicant
    lik = p ** Y[None, :] * (1 - p) ** (1 - Y[None, :])  # (n_samples, n)

    # average over noise samples, then log and sum over applicants
    return np.sum(np.log(lik.mean(axis=0)))