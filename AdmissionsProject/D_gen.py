import numpy as np
import pandas as pd


def generate_applicant_dataset(
    total_applicants: int,
    white_proportion: float,
    means: dict,    # {"white": {"gpa": , "sat": }, "asian": {...}}
    stds:  dict,    # same structure
    gpa_weight: float,
    sat_weight: float,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate applicant dataset for White and Asian American applicants.

    Q is computed from GPA and SAT only (normalized to [0,100]).
    Essays are excluded from Q — they enter the model as noise instead.
    """
    rng = np.random.default_rng(seed)

    n_white = round(total_applicants * white_proportion)
    n_asian = total_applicants - n_white

    def sample(mean, std, size, lo, hi):
        return np.clip(rng.normal(mean, std, size), lo, hi)

    rows = []
    for race, z, n, m, s in [
        ("White",          0, n_white, means["white"], stds["white"]),
        ("Asian American", 1, n_asian, means["asian"], stds["asian"]),
    ]:
        rows.append(pd.DataFrame({
            "race": race,
            "Z":    z,
            "GPA":  sample(m["gpa"], s["gpa"], n, 0,   4.0),
            "SAT":  sample(m["sat"], s["sat"], n, 400, 1600),
        }))

    df = pd.concat(rows, ignore_index=True)

    # Normalize to [0, 100]
    df["GPA_norm"] = df["GPA"] / 4.0 * 100
    df["SAT_norm"] = (df["SAT"] - 400) / 1200 * 100

    # Weighted Q from GPA and SAT only
    total_w = gpa_weight + sat_weight
    wg = gpa_weight / total_w
    ws = sat_weight  / total_w
    df["Q"] = wg * df["GPA_norm"] + ws * df["SAT_norm"]

    return df