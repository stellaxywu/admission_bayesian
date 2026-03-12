import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from D_gen  import generate_applicant_dataset
from admissions_func import simulate_admissions
from bayesian   import compute_posterior
from dataset  import DATASETS

# ---------------------------------------------------------------
# HARDCODED INTERNALS
# ---------------------------------------------------------------
BETA1      = 0.5   # log-odds per 1 SD of Q (Q is standardized)
STDS       = {
    "white": {"gpa": 0.22, "sat": 120},
    "asian": {"gpa": 0.15, "sat": 120},
}
GAMMA_GRID = np.linspace(-3, 3, 200)

# ---------------------------------------------------------------
# SESSION STATE DEFAULTS
# ---------------------------------------------------------------
_DEFAULTS = {
    "eg_total":      25000,
    "eg_wprop":      0.77,
    "eg_aprop":      0.06,
    "eg_wgpa":       3.90,  "eg_agpa":  3.80,
    "eg_wsat":       1350,  "eg_asat":  1400,
    "eg_wadmit":     62.0,  "eg_aadmit": 54.0,
    "eg_w_gpa_std":  0.22,  "eg_a_gpa_std": 0.15,
    "eg_w_sat_std":  120,   "eg_a_sat_std": 120,
}
for _k, _v in _DEFAULTS.items():
    st.session_state.setdefault(_k, _v)

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="Admissions Bias Estimator", layout="wide")
st.title("Admissions Bias Estimator")
st.markdown(
    "This tool estimates the probability of racial bias in college admissions. "
    "The qualification score **Q** is built from GPA and SAT only. "
    "Essays and other holistic factors enter as **noise** — reflecting genuine "
    "uncertainty about unobserved admission criteria."
)

# ---------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------
st.sidebar.header("Score Weights")
w_gpa = st.sidebar.slider("GPA weight", 0.0, 1.0, 0.5, 0.05)
w_sat = st.sidebar.slider("SAT weight", 0.0, 1.0, 0.5, 0.05)
if w_gpa + w_sat == 0:
    st.sidebar.error("At least one weight must be nonzero.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("Unobserved Confounders")
st.sidebar.markdown(
    "Unobserved factors (legacy status, athletic recruitment, geography) "
    "may correlate with race **and** affect admission, partially explaining "
    "the admit rate gap without implying direct discrimination."
)
delta = st.sidebar.slider(
    "Confounder advantage δ (white vs Asian)",
    0.0, 2.0, 0.0, 0.05,
    help="Mean log-odds advantage for white applicants from unobserved factors. "
         "δ=0: unobserved factors are race-neutral. "
         "δ=0.5: white applicants gain ~0.5 log-odds on average from legacy/athletics/etc. "
         "As δ increases, less of the admit rate gap is attributed to γ."
)
sigma_u = st.sidebar.slider(
    "Confounder noise σ (individual variation)",
    0.0, 2.0, 0.3, 0.05,
    help="Within-group SD of unobserved factors. "
         "Higher σ = more individual variation in essays/extracurriculars/etc., "
         "widening the posterior on γ."
)
st.sidebar.markdown("---")
st.sidebar.header("Simulation Noise")
sigma_noise = st.sidebar.slider(
    "Simulation noise σ (Estimating Admit Rates only)",
    0.0, 2.0, 0.3, 0.1,
    help="Individual noise used in the forward simulation tab only. "
         "Does not affect the Estimating Gamma posterior."
)


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def make_df(total, white_prop, asian_prop, means, stds):
    df = generate_applicant_dataset(
        total_applicants = total,
        white_proportion = white_prop,
        asian_proportion = asian_prop,
        means            = means,
        stds             = stds,
        gpa_weight       = w_gpa,
        sat_weight       = w_sat,
    )
    df["Q"] = (df["Q"] - df["Q"].mean()) / df["Q"].std()
    return df


def draw_Y_from_rates(df, white_admit, asian_admit):
    rng = np.random.default_rng(42)
    df  = df.copy()
    df["Y"] = 0
    df.loc[df["Z"] == 0, "Y"] = rng.binomial(1, white_admit, (df["Z"] == 0).sum())
    df.loc[df["Z"] == 1, "Y"] = rng.binomial(1, asian_admit, (df["Z"] == 1).sum())
    return df


def show_admit_summary(df):
    admitted    = df[df["Y"] == 1]
    white_df    = df[df["Z"] == 0]
    asian_df    = df[df["Z"] == 1]
    white_share = white_df["Y"].sum() / max(len(admitted), 1)
    asian_share = asian_df["Y"].sum() / max(len(admitted), 1)

    m1, m2, m3 = st.columns(3)
    m1.metric("Overall admit rate",            f"{df['Y'].mean():.1%}")
    m2.metric("White admit rate",              f"{white_df['Y'].mean():.1%}")
    m3.metric("Asian American admit rate",     f"{asian_df['Y'].mean():.1%}")

    m4, m5, m6 = st.columns(3)
    m4.metric("Total admitted",                f"{len(admitted):,}")
    m5.metric("White share of admitted class", f"{white_share:.1%}")
    m6.metric("Asian share of admitted class", f"{asian_share:.1%}")


def show_posterior(df, beta0):
    with st.spinner("Computing posterior..."):
        gamma_grid, posterior, p_neg = compute_posterior(
            df, beta0=beta0, beta1=BETA1,
            prior_std=1.0,
            delta=delta,
            sigma_u=sigma_u,
            gamma_grid=GAMMA_GRID
        )

    st.metric("P(γ < 0 | D)", f"{p_neg:.4f}")

    if p_neg > 0.95:
        st.error("Strong evidence of a penalty against Asian American applicants.")
    elif p_neg > 0.8:
        st.warning("Moderate evidence of a penalty against Asian American applicants.")
    elif p_neg > 0.5:
        st.info("Weak evidence of a penalty — results inconclusive.")
    else:
        st.success("No meaningful evidence of bias detected.")

    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.plot(gamma_grid, posterior, color="#5b9bd5", linewidth=2)
    ax.axvline(0, color="black", linestyle="--", linewidth=1, label="γ = 0")
    ax.fill_between(
        gamma_grid[gamma_grid < 0], posterior[gamma_grid < 0],
        alpha=0.25, color="red", label=f"P(γ < 0) = {p_neg:.4f}"
    )
    ax.set_xlabel("γ"); ax.set_ylabel("Posterior density")
    ax.set_title("Posterior Distribution of γ")
    ax.legend(fontsize=8); ax.set_facecolor("#f9f9f9")
    fig.tight_layout()
    st.pyplot(fig)


def proportion_sliders(col, wp_key, ap_key, wp_default=0.77, ap_default=0.06):
    """Two independent proportion sliders that validate they don't exceed 1.0."""
    with col:
        wp = st.slider("White proportion",         0.01, 0.99, step=0.01, key=wp_key)
        ap = st.slider("Asian American proportion", 0.01, 0.99, step=0.01, key=ap_key)
        total = wp + ap
        if total > 1.0:
            st.error(f"White ({wp:.0%}) + Asian ({ap:.0%}) = {total:.0%} — must not exceed 100%.")
            st.stop()
        st.caption(f"Other groups: {1 - total:.0%} of applicant pool")
    return wp, ap


# ================================================================
# TABS
# ================================================================
tab_eg, tab_ear = st.tabs(["Estimating Gamma", "Estimating Admit Rates"])


# ================================================================
# TAB 1 — ESTIMATING GAMMA
# ================================================================
with tab_eg:
    st.subheader("Estimating Gamma")
    st.markdown(
        "Input observed admit rates by race. The model infers **γ** — the bias indicator — "
        "from the admit rate disparity after accounting for GPA and SAT differences. "
        "Use the sidebar to control **unobserved confounders** (legacy, athletics, geography): "
        "raising **δ** shifts credit for the gap away from γ toward race-correlated but "
        "non-discriminatory factors. Raising **σ** widens the posterior to reflect individual variation."
    )

    # Dataset loader
    dataset_labels = ["— Enter manually —"] + [d["label"] for d in DATASETS]
    selected = st.selectbox("Load a dataset", dataset_labels, key="eg_selected")

    if selected != "— Enter manually —":
        d = next(x for x in DATASETS if x["label"] == selected)
        st.session_state["eg_total"]     = d["total_applicants"]
        st.session_state["eg_wprop"]     = float(d["white_proportion"])
        st.session_state["eg_aprop"]     = float(d["asian_proportion"])
        st.session_state["eg_wgpa"]      = float(d["white_gpa_mean"])
        st.session_state["eg_agpa"]      = float(d["asian_gpa_mean"])
        st.session_state["eg_wsat"]      = int(d["white_sat_mean"])
        st.session_state["eg_asat"]      = int(d["asian_sat_mean"])
        st.session_state["eg_wadmit"]    = round(d["white_admit_rate"] * 100, 1)
        st.session_state["eg_aadmit"]    = round(d["asian_admit_rate"] * 100, 1)
        st.session_state["eg_w_gpa_std"] = d["white_gpa_std"]
        st.session_state["eg_a_gpa_std"] = d["asian_gpa_std"]
        st.session_state["eg_w_sat_std"] = d["white_sat_std"]
        st.session_state["eg_a_sat_std"] = d["asian_sat_std"]

    c1, c2, c3 = st.columns(3)

    with c1:
        eg_total = st.number_input("Total applicants", 100, 150000, step=1000, key="eg_total")
        eg_wprop = st.slider("White proportion",          0.01, 0.99, step=0.01, key="eg_wprop")
        eg_aprop = st.slider("Asian American proportion", 0.01, 0.99, step=0.01, key="eg_aprop")
        eg_combined = eg_wprop + eg_aprop
        if eg_combined > 1.0:
            st.error(f"White ({eg_wprop:.0%}) + Asian ({eg_aprop:.0%}) = {eg_combined:.0%} — must not exceed 100%.")
            st.stop()
        st.caption(f"Other groups: {1 - eg_combined:.0%} of applicant pool")

    with c2:
        st.markdown("**White Applicants**")
        eg_wgpa   = st.number_input("Mean GPA", 0.0, 4.0,  step=0.01, key="eg_wgpa")
        eg_wsat   = st.number_input("Mean SAT", 400, 1600, step=10,   key="eg_wsat")
        eg_wadmit = st.slider("Admit rate (%)", 0.1, 100.0, step=0.1, key="eg_wadmit") / 100

    with c3:
        st.markdown("**Asian American Applicants**")
        eg_agpa   = st.number_input("Mean GPA", 0.0, 4.0,  step=0.01, key="eg_agpa")
        eg_asat   = st.number_input("Mean SAT", 400, 1600, step=10,   key="eg_asat")
        eg_aadmit = st.slider("Admit rate (%)", 0.1, 100.0, step=0.1, key="eg_aadmit") / 100

    if st.button("Estimate γ", type="primary", key="eg_run"):
        means = {
            "white": {"gpa": eg_wgpa, "sat": eg_wsat},
            "asian": {"gpa": eg_agpa, "sat": eg_asat},
        }
        stds = {
            "white": {"gpa": st.session_state["eg_w_gpa_std"], "sat": st.session_state["eg_w_sat_std"]},
            "asian": {"gpa": st.session_state["eg_a_gpa_std"], "sat": st.session_state["eg_a_sat_std"]},
        }
        df = make_df(int(eg_total), eg_wprop, eg_aprop, means, stds)
        df = draw_Y_from_rates(df, eg_wadmit, eg_aadmit)

        # beta0 is calibrated to the admit rate within the modeled subgroup
        # (white + asian only). Other racial groups are not modeled and do
        # not affect inference — the effective pool is n_white + n_asian.
        n_modeled = len(df)
        n_total   = int(eg_total)
        overall   = df["Y"].mean()
        beta0     = np.log(overall / (1 - overall))

        st.caption(
            f"Modelling {n_modeled:,} of {n_total:,} applicants "
            f"({n_modeled/n_total:.0%} — white + Asian American only). "
            f"Other groups are excluded from inference."
        )

        st.markdown("---")
        show_admit_summary(df)
        st.markdown("---")
        show_posterior(df, beta0)

        st.markdown("---")
        st.subheader("Score Summary")
        st.dataframe(
            df.groupby("race")[["GPA", "SAT", "Q"]]
            .mean().round(2).rename(columns={"Q": "Q (centered)"})
        )


# ================================================================
# TAB 2 — ESTIMATING ADMIT RATES
# ================================================================
with tab_ear:
    st.subheader("Estimating Admit Rates")
    st.markdown(
        "Input applicant pool parameters. The model shows expected admission "
        "outcomes under three worlds: **no bias** (γ = 0), **moderate bias** "
        "(γ = −0.5), and **strong bias** (γ = −0.8) against Asian American applicants."
    )

    e1, e2, e3 = st.columns(3)
    with e1:
        ear_total    = st.number_input("Total applicants", 100, 150000, 25000, 1000, key="ear_total")
        ear_wprop    = st.slider("White proportion",          0.01, 0.99, 0.77, 0.01, key="ear_wprop")
        ear_aprop    = st.slider("Asian American proportion", 0.01, 0.99, 0.06, 0.01, key="ear_aprop")
        ear_combined = ear_wprop + ear_aprop
        if ear_combined > 1.0:
            st.error(f"White ({ear_wprop:.0%}) + Asian ({ear_aprop:.0%}) = {ear_combined:.0%} — must not exceed 100%.")
            st.stop()
        st.caption(f"Other groups: {1 - ear_combined:.0%} of applicant pool")
        ear_baseline = st.slider("Baseline admit rate (%)", 1, 100, 60, 1, key="ear_baseline") / 100

    with e2:
        st.markdown("**White Applicants**")
        ear_wgpa = st.number_input("Mean GPA", 0.0, 4.0,  3.90, 0.01, key="ear_wgpa")
        ear_wsat = st.number_input("Mean SAT", 400, 1600, 1350, 10,   key="ear_wsat")

    with e3:
        st.markdown("**Asian American Applicants**")
        ear_agpa = st.number_input("Mean GPA", 0.0, 4.0,  3.80, 0.01, key="ear_agpa")
        ear_asat = st.number_input("Mean SAT", 400, 1600, 1400, 10,   key="ear_asat")

    if st.button("Run", type="primary", key="ear_run"):
        means = {
            "white": {"gpa": ear_wgpa, "sat": ear_wsat},
            "asian": {"gpa": ear_agpa, "sat": ear_asat},
        }
        df_base = make_df(int(ear_total), ear_wprop, ear_aprop, means, STDS)
        beta0   = np.log(ear_baseline / (1 - ear_baseline))

        n_modeled = len(df_base)
        st.caption(
            f"Modelling {n_modeled:,} of {int(ear_total):,} applicants "
            f"({n_modeled/int(ear_total):.0%} — white + Asian American only). "
            f"Other groups are excluded from inference."
        )
        st.markdown("---")
        col0, col1, col2 = st.columns(3)

        gammas       = [0.0, -0.5, -0.8]
        labels       = ["γ = 0", "γ = −0.5", "γ = −0.8"]
        white_rates  = []
        asian_rates  = []
        white_shares = []
        asian_shares = []

        for col, gamma, label in zip([col0, col1, col2], gammas, labels):
            df_g     = simulate_admissions(
                df_base, beta0=beta0, beta1=BETA1,
                gamma=gamma, sigma_noise=sigma_noise
            )
            admitted    = df_g[df_g["Y"] == 1]
            white_df    = df_g[df_g["Z"] == 0]
            asian_df    = df_g[df_g["Z"] == 1]
            w_rate      = white_df["Y"].mean()
            a_rate      = asian_df["Y"].mean()
            w_share     = white_df["Y"].sum() / max(len(admitted), 1)
            a_share     = asian_df["Y"].sum() / max(len(admitted), 1)

            white_rates.append(w_rate)
            asian_rates.append(a_rate)
            white_shares.append(w_share)
            asian_shares.append(a_share)

            with col:
                st.markdown(f"### {label}")
                st.metric("Overall admit rate",   f"{df_g['Y'].mean():.1%}")
                st.metric("White admit rate",     f"{w_rate:.1%}")
                st.metric("Asian admit rate",     f"{a_rate:.1%}")
                st.metric("Total admitted",       f"{len(admitted):,}")
                st.metric("White share of class", f"{w_share:.1%}")
                st.metric("Asian share of class", f"{a_share:.1%}")

        # ---- Chart ----
        st.markdown("---")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        x     = np.arange(len(labels))
        width = 0.35

        ax1.bar(x - width/2, [r * 100 for r in white_rates], width,
                label="White", color="#5b9bd5")
        ax1.bar(x + width/2, [r * 100 for r in asian_rates], width,
                label="Asian American", color="#c8a96e")
        ax1.set_xticks(x); ax1.set_xticklabels(labels)
        ax1.set_ylabel("Admit Rate (%)"); ax1.set_title("Admit Rate by Race")
        ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
        ax1.set_facecolor("#f9f9f9")
        for i, (w, a) in enumerate(zip(white_rates, asian_rates)):
            ax1.text(i - width/2, w * 100 + 0.2, f"{w:.1%}", ha="center", fontsize=8)
            ax1.text(i + width/2, a * 100 + 0.2, f"{a:.1%}", ha="center", fontsize=8)

        ax2.bar(x - width/2, [s * 100 for s in white_shares], width,
                label="White", color="#5b9bd5")
        ax2.bar(x + width/2, [s * 100 for s in asian_shares], width,
                label="Asian American", color="#c8a96e")
        ax2.set_xticks(x); ax2.set_xticklabels(labels)
        ax2.set_ylabel("Share of Admitted Class (%)")
        ax2.set_title("Share of Admitted Class by Race")
        ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
        ax2.set_facecolor("#f9f9f9")
        for i, (w, a) in enumerate(zip(white_shares, asian_shares)):
            ax2.text(i - width/2, w * 100 + 0.5, f"{w:.1%}", ha="center", fontsize=8)
            ax2.text(i + width/2, a * 100 + 0.5, f"{a:.1%}", ha="center", fontsize=8)

        fig.tight_layout()
        fig.subplots_adjust(bottom=0.18)
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("Score Summary")
        st.dataframe(
            df_base.groupby("race")[["GPA", "SAT", "Q"]]
            .mean().round(2).rename(columns={"Q": "Q (centered)"})
        )