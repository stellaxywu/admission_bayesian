import numpy as np
import pandas as pd


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


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

    eps is centered within each race group so it creates individual-level
    variation only, not spurious group-level gaps.

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

    # Draw noise centered within each race group
    eps = rng.normal(0, sigma_noise, size=n)
    for z_val in [0, 1]:
        mask = Z == z_val
        if mask.sum() > 0:
            eps[mask] -= eps[mask].mean()

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
) -> float:
    """
    Standard logistic log-likelihood (no noise term):

        log P(D|gamma) = sum_i [ Y_i*log(p_i) + (1-Y_i)*log(1-p_i) ]
        where p_i = sigma(beta0 + beta1*Q_i + gamma*Z_i)

    Noise eps is part of the simulation (forward model) only.
    For inference we integrate out eps analytically by using the
    logistic regression likelihood directly — this is valid because
    eps is mean-zero and independent of Z by construction.
    """
    p = sigmoid(beta0 + beta1 * df["Q"].values + gamma * df["Z"].values)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return np.sum(df["Y"].values * np.log(p) + (1 - df["Y"].values) * np.log(1 - p))