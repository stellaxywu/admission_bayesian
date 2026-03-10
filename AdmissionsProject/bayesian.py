import numpy as np
import pandas as pd

from admissions_func import log_likelihood


def compute_posterior(
    df: pd.DataFrame,
    beta0: float,
    beta1: float,
    sigma_noise: float,
    gamma_grid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Numerically approximate P(gamma | D) on a discrete grid.

    Prior:   gamma ~ N(0, 1)
    Likelihood integrates out noise via Monte Carlo (see admissions.py)

    Returns:
        gamma_grid  : gamma values evaluated
        posterior   : normalized posterior density
        p_gamma_neg : P(gamma < 0 | D)
    """
    sigma = 2.0
    log_prior = -0.5 * (gamma_grid / sigma) ** 2
    log_lik   = np.array([
        log_likelihood(g, df, beta0, beta1, sigma_noise)
        for g in gamma_grid
    ])

    log_unnorm = log_prior + log_lik
    log_unnorm -= log_unnorm.max()
    unnorm     = np.exp(log_unnorm)

    posterior   = unnorm / np.trapezoid(unnorm, gamma_grid)
    p_gamma_neg = np.trapezoid(posterior[gamma_grid < 0], gamma_grid[gamma_grid < 0])

    return gamma_grid, posterior, p_gamma_neg