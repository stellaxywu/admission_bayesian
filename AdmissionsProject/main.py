import numpy as np
import pandas as pd

from D_gen import generate_applicant_dataset
from bayesian import compute_posterior


# ---------------------------------------------------------------
# HARDCODED INTERNALS (derived from Harvard admissions data)
# ---------------------------------------------------------------
BETA1 = 0.03
STDS  = {
    "white": {"gpa": 0.24, "sat": 130, "essay": 10},
    "asian": {"gpa": 0.20, "sat": 125, "essay": 10},
}


# ---------------------------------------------------------------
# USER INPUTS — only edit this section
# ---------------------------------------------------------------
MODE = "real"   # "real" or "simulation"

REAL = dict(
    total_applicants = 45000,
    white_proportion = 0.60,
    means   = {"white": {"gpa": 3.85, "sat": 1340, "essay": 78},
               "asian": {"gpa": 3.80, "sat": 1400, "essay": 76}},
    weights = {"gpa": 0.4, "sat": 0.4, "essay": 0.2},
    white_admit_rate = 0.18,
    asian_admit_rate = 0.12,
)

SIM = dict(
    total_applicants = 45000,
    white_proportion = 0.60,
    means   = {"white": {"gpa": 3.85, "sat": 1340, "essay": 78},
               "asian": {"gpa": 3.80, "sat": 1400, "essay": 76}},
    weights = {"gpa": 0.4, "sat": 0.4, "essay": 0.2},
    white_admit_rate = 0.20,
    asian_admit_rate = 0.10,
)
# ---------------------------------------------------------------


def run(cfg, mode_label):
    df = generate_applicant_dataset(
        total_applicants = cfg["total_applicants"],
        white_proportion = cfg["white_proportion"],
        means            = cfg["means"],
        stds             = STDS,
        weights          = cfg["weights"],
    )
    df["Q"] = df["Q"] - df["Q"].mean()

    # Draw Y from admit rates — gamma is never specified, always inferred
    rng = np.random.default_rng(42)
    df["Y"] = 0
    df.loc[df["Z"] == 0, "Y"] = rng.binomial(1, cfg["white_admit_rate"], (df["Z"] == 0).sum())
    df.loc[df["Z"] == 1, "Y"] = rng.binomial(1, cfg["asian_admit_rate"], (df["Z"] == 1).sum())

    overall_rate = df["Y"].mean()
    beta0 = np.log(overall_rate / (1 - overall_rate))

    # --- Summary ---
    print(f"Mode: {mode_label}  |  N = {cfg['total_applicants']:,}")
    print(df.groupby("race")[["GPA", "SAT", "Essay", "Q"]].mean().round(2))
    print()
    admitted = df[df["Y"] == 1]
    print(f"Overall admit rate: {overall_rate:.3f}  ({len(admitted):,} admitted)")
    for race, group in df.groupby("race"):
        pct_of_class = group["Y"].sum() / len(admitted)
        print(f"  {race}: admit rate {group['Y'].mean():.3f}, {pct_of_class:.3f} of admitted class")
    print()

    # --- Bayesian posterior for gamma ---
    gamma_grid = np.linspace(-3, 3, 500)
    _, _, p_neg = compute_posterior(df, beta0=beta0, beta1=BETA1, gamma_grid=gamma_grid)
    print(f"P(gamma < 0 | D) = {p_neg:.4f}")
    print()


if MODE == "real":
    run(REAL, "Real Data")
elif MODE == "simulation":
    run(SIM, "Simulation")