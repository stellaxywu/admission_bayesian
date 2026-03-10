# ---------------------------------------------------------------
# REAL WORLD DATASETS — University of Michigan
#
# TO ADD A NEW DATASET:
# Copy one of the existing entries below and update the values.
# The new dataset will automatically appear in the app dropdown.
#
# Fields:
#   label            : display name shown in the UI dropdown
#   total_applicants : total applicant pool size
#   white_proportion : fraction of applicants who are White (0-1)
#   white_gpa_mean   : median GPA for White admittees
#   asian_gpa_mean   : median GPA for Asian American admittees
#   white_gpa_std    : GPA standard deviation for White applicants
#   asian_gpa_std    : GPA standard deviation for Asian American applicants
#   white_sat_mean   : median SAT for White admittees
#   asian_sat_mean   : median SAT for Asian American admittees
#   white_sat_std    : SAT standard deviation for White applicants
#   asian_sat_std    : SAT standard deviation for Asian American applicants
#   white_essay_mean : essay mean for White applicants (0-100)
#   asian_essay_mean : essay mean for Asian American applicants (0-100)
#   white_admit_rate : observed admit rate for White applicants (0-1)
#   asian_admit_rate : observed admit rate for Asian American applicants (0-1)
# ---------------------------------------------------------------

DATASETS = [
    {
        "label":            "U of Michigan 1999",
        "total_applicants": 16138,
        "white_proportion": 0.77,
        "white_gpa_mean":   3.80,
        "asian_gpa_mean":   3.70,
        "white_gpa_std":    0.22,
        "asian_gpa_std":    0.30,
        "white_sat_mean":   1310,
        "asian_sat_mean":   1360,
        "white_sat_std":    126,
        "asian_sat_std":    115,
        "white_essay_mean": 78,
        "asian_essay_mean": 78,
        "white_admit_rate": 0.66,
        "asian_admit_rate": 0.58,
    },
    {
        "label":            "U of Michigan 2003",
        "total_applicants": 19482,
        "white_proportion": 0.77,
        "white_gpa_mean":   3.90,
        "asian_gpa_mean":   3.90,
        "white_gpa_std":    0.22,
        "asian_gpa_std":    0.22,
        "white_sat_mean":   1340,
        "asian_sat_mean":   1380,
        "white_sat_std":    119,
        "asian_sat_std":    119,
        "white_essay_mean": 78,
        "asian_essay_mean": 78,
        "white_admit_rate": 0.57,
        "asian_admit_rate": 0.43,
    },
    {
        "label":            "U of Michigan 2004",
        "total_applicants": 15597,
        "white_proportion": 0.77,
        "white_gpa_mean":   3.80,
        "asian_gpa_mean":   3.80,
        "white_gpa_std":    0.22,
        "asian_gpa_std":    0.15,
        "white_sat_mean":   1340,
        "asian_sat_mean":   1380,
        "white_sat_std":    126,
        "asian_sat_std":    126,
        "white_essay_mean": 78,
        "asian_essay_mean": 78,
        "white_admit_rate": 0.68,
        "asian_admit_rate": 0.58,
    },
    {
        "label":            "U of Michigan 2005",
        "total_applicants": 18198,
        "white_proportion": 0.77,
        "white_gpa_mean":   3.90,
        "asian_gpa_mean":   3.80,
        "white_gpa_std":    0.22,
        "asian_gpa_std":    0.15,
        "white_sat_mean":   1350,
        "asian_sat_mean":   1400,
        "white_sat_std":    119,
        "asian_sat_std":    119,
        "white_essay_mean": 78,
        "asian_essay_mean": 78,
        "white_admit_rate": 0.62,
        "asian_admit_rate": 0.54,
    },
    # ---- ADD NEW DATASETS BELOW THIS LINE ----
    # {
    #     "label":            "My University YYYY",
    #     "total_applicants": 30000,
    #     "white_proportion": 0.70,
    #     "white_gpa_mean":   3.80,
    #     "asian_gpa_mean":   3.85,
    #     "white_gpa_std":    0.22,
    #     "asian_gpa_std":    0.15,
    #     "white_sat_mean":   1320,
    #     "asian_sat_mean":   1400,
    #     "white_sat_std":    120,
    #     "asian_sat_std":    120,
    #     "white_essay_mean": 78,
    #     "asian_essay_mean": 78,
    #     "white_admit_rate": 0.60,
    #     "asian_admit_rate": 0.50,
    # },
]