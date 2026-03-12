import numpy as np
import pandas as pd

from admissions_func import sigmoid


def log_lik_confounder(
    gamma: float,
    df: pd.DataFrame,
    beta0: float,
    beta1: float,
    delta: float,
    sigma_u: float,
    n_mc: int = 200,
    max_n: int = 2000,
    seed: int = 1,
) -> float:
    """
    Marginal log-likelihood integrating out the unobserved confounder U:

        P(Y_i=1 | Q, Z, gamma) = E_U[ sigma(beta0 + beta1*Q + gamma*Z + U) ]
        U_i ~ N(delta*(0.5 - Z_i), sigma_u^2)
            white (Z=0): U ~ N(+delta/2, sigma_u^2)
            asian (Z=1): U ~ N(-delta/2, sigma_u^2)

    delta   : mean confounder advantage for white applicants in log-odds.
              Represents race-correlated unobserved factors (legacy, athletics).
              Raising delta shifts the admit gap away from gamma onto U.
    sigma_u : within-group SD of unobserved factors (individual variation).
    max_n   : subsample size — log-likelihood is scaled back to full n for speed.
    """
    Q = df["Q"].values
    Z = df["Z"].values
    Y = df["Y"].values
    n = len(df)

    rng = np.random.default_rng(seed)

    # Subsample proportionally (preserving race balance) for speed
    if n > max_n:
        # Stratified subsample: preserve white/asian ratio
        idx_w = np.where(Z == 0)[0]
        idx_a = np.where(Z == 1)[0]
        n_w = int(max_n * len(idx_w) / n)
        n_a = max_n - n_w
        idx = np.concatenate([
            rng.choice(idx_w, min(n_w, len(idx_w)), replace=False),
            rng.choice(idx_a, min(n_a, len(idx_a)), replace=False),
        ])
        Q, Z, Y = Q[idx], Z[idx], Y[idx]
        scale = n / len(idx)
    else:
        scale = 1.0

    n_sub = len(Y)

    # Degenerate: no confounder — standard logistic
    if sigma_u < 1e-6 and abs(delta) < 1e-6:
        p = np.clip(sigmoid(beta0 + beta1 * Q + gamma * Z), 1e-12, 1 - 1e-12)
        return float(scale * np.sum(Y * np.log(p) + (1 - Y) * np.log(1 - p)))

    mu_u = delta * (0.5 - Z)                                         # (n_sub,)
    U    = rng.normal(0, max(sigma_u, 1e-6), (n_mc, n_sub)) + mu_u  # (n_mc, n_sub)
    eta  = beta0 + beta1 * Q[None, :] + gamma * Z[None, :] + U
    p    = np.clip(sigmoid(eta), 1e-12, 1 - 1e-12)

    ll   = Y[None, :] * np.log(p) + (1 - Y[None, :]) * np.log(1 - p)
    mx   = ll.max(axis=0)
    return float(scale * np.sum(np.log(np.exp(ll - mx).mean(axis=0)) + mx))


def compute_posterior(
    df: pd.DataFrame,
    beta0: float,
    beta1: float,
    prior_std: float,
    delta: float,
    sigma_u: float,
    gamma_grid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Approximate P(gamma | D) on a discrete grid.

    Prior:      gamma ~ N(0, prior_std^2)
    Likelihood: marginalizes over unobserved confounder U (see log_lik_confounder)

    delta     : mean white confounder advantage (log-odds). Slides credit for
                the admit gap between gamma (discrimination) and U (structural).
    sigma_u   : individual variation in unobserved factors (widens posterior).
    prior_std : prior SD on gamma. With large N this has minimal effect vs delta/sigma_u.
    """
    log_prior = -0.5 * (gamma_grid / max(prior_std, 0.01)) ** 2

    log_lik = np.array([
        log_lik_confounder(g, df, beta0, beta1, delta, sigma_u)
        for g in gamma_grid
    ])

    log_unnorm = log_prior + log_lik
    log_unnorm -= log_unnorm.max()
    unnorm = np.exp(log_unnorm)

    posterior   = unnorm / np.trapezoid(unnorm, gamma_grid)
    p_gamma_neg = float(np.trapezoid(
        posterior[gamma_grid < 0], gamma_grid[gamma_grid < 0]
    ))

    return gamma_grid, posterior, p_gamma_neg