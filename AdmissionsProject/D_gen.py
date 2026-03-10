import numpy as np
import pandas as pd


def generate_applicant_dataset(
    total_applicants: int,
    white_proportion: float,
    means: dict,       # {"white": {"gpa": , "sat": , "essay": }, "asian": {...}}
    variances: dict,   # same structure
    weights: dict,     # {"gpa": , "sat": , "essay": }
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate applicant dataset for White and Asian American applicants.

    Scores are normalized to [0, 100] and combined into a weighted
    qualification score Q.
    """
    rng = np.random.default_rng(seed)

    n_white = round(total_applicants * white_proportion)
    n_asian = total_applicants - n_white

    def sample(mean, var, size, lo, hi):
        return np.clip(rng.normal(mean, np.sqrt(var), size), lo, hi)

    rows = []
    for race, z, n, m, v in [
        ("White",          0, n_white, means["white"],  variances["white"]),
        ("Asian American", 1, n_asian, means["asian"],  variances["asian"]),
    ]:
        rows.append(pd.DataFrame({
            "race":  race,
            "Z":     z,
            "GPA":   sample(m["gpa"],   v["gpa"],   n, 0,   4.0),
            "SAT":   sample(m["sat"],   v["sat"],   n, 400, 1600),
            "Essay": sample(m["essay"], v["essay"], n, 0,   100),
        }))

    df = pd.concat(rows, ignore_index=True)

    # Normalize each metric to [0, 100]
    df["GPA_norm"]   = df["GPA"] / 4.0 * 100
    df["SAT_norm"]   = (df["SAT"] - 400) / 1200 * 100
    df["Essay_norm"] = df["Essay"]

    # Weighted qualification score (weights auto-normalized to sum to 1)
    w = np.array([weights["gpa"], weights["sat"], weights["essay"]], dtype=float)
    w /= w.sum()
    df["Q"] = w[0]*df["GPA_norm"] + w[1]*df["SAT_norm"] + w[2]*df["Essay_norm"]

    return df


# if __name__ == "__main__":
#     df = generate_applicant_dataset(
#         total_applicants=1000,
#         white_proportion=0.60,
#         means={
#             "white": {"gpa": 3.70, "sat": 1350, "essay": 78},
#             "asian": {"gpa": 3.80, "sat": 1450, "essay": 76},
#         },
#         variances={
#             "white": {"gpa": 0.04, "sat": 10000, "essay": 64},
#             "asian": {"gpa": 0.03, "sat":  8100, "essay": 81},
#         },
#         weights={"gpa": 0.4, "sat": 0.4, "essay": 0.2},
#     )

#     print(df.head())
#     print()
#     print(df.groupby("race")[["GPA", "SAT", "Essay", "Q"]].mean().round(2))