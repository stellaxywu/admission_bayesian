# ---------------------------------------------------------------
# DATASETS
#
# Sources:
#   University of Michigan: University admissions records
#   Harvard Class of 2000-2017: Trial Exhibit DX042, SFFA v. Harvard
#     - Apps, Admits, % of Apps taken directly from DX042.0001-0003
#     - Admit rates computed as Admits/Apps
#     - SAT figures from DX042.0010-0011 (SAT section averages, old methodology)
#       DX042 reports average SAT II section scores (out of 800).
#       Converted to total SAT (1600 scale): score * 2 (two-section approximation).
#       SAT stds estimated as 130 pts for Asian Am, 140 pts for White applicants
#       (consistent with Harvard's reported interquartile spread in litigation docs).
#     - GPA data not in DX042; estimated from Arcidiacono et al. (2022):
#       Asian applicants score ~0.05 SD higher than White on academic index.
#       Harvard applicant GPA means estimated ~3.85 (White), ~3.89 (Asian).
#       GPA stds from typical selective-school distributions.
#
#   Harvard Class of 2018-2020: Harvard does not publish race-stratified admit
#     rates post-DX042. These entries are omitted (no credible source).
#
# white_proportion and asian_proportion are INDEPENDENT fractions of the
# total applicant pool. They do NOT need to sum to 1.
#
# TO ADD A NEW DATASET: copy the template at the bottom.
# ---------------------------------------------------------------

DATASETS = [

    # ================================================================
    # UNIVERSITY OF MICHIGAN (admissions records 1999-2005)
    # ================================================================
    {
        "label":            "U of Michigan 1999",
        "total_applicants": 16138,
        "white_proportion": 0.770,
        "asian_proportion": 0.140,
        "white_gpa_mean":   3.80, "white_gpa_std": 0.22,
        "asian_gpa_mean":   3.70, "asian_gpa_std": 0.30,
        "white_sat_mean":   1310, "white_sat_std": 126,
        "asian_sat_mean":   1360, "asian_sat_std": 115,
        "white_admit_rate": 0.660,
        "asian_admit_rate": 0.580,
    },
    {
        "label":            "U of Michigan 2003",
        "total_applicants": 19482,
        "white_proportion": 0.720,
        "asian_proportion": 0.180,
        "white_gpa_mean":   3.90, "white_gpa_std": 0.22,
        "asian_gpa_mean":   3.90, "asian_gpa_std": 0.22,
        "white_sat_mean":   1340, "white_sat_std": 119,
        "asian_sat_mean":   1380, "asian_sat_std": 119,
        "white_admit_rate": 0.570,
        "asian_admit_rate": 0.430,
    },
    {
        "label":            "U of Michigan 2004",
        "total_applicants": 15597,
        "white_proportion": 0.720,
        "asian_proportion": 0.180,
        "white_gpa_mean":   3.80, "white_gpa_std": 0.22,
        "asian_gpa_mean":   3.80, "asian_gpa_std": 0.15,
        "white_sat_mean":   1340, "white_sat_std": 126,
        "asian_sat_mean":   1380, "asian_sat_std": 126,
        "white_admit_rate": 0.680,
        "asian_admit_rate": 0.580,
    },
    {
        "label":            "U of Michigan 2005",
        "total_applicants": 18198,
        "white_proportion": 0.710,
        "asian_proportion": 0.190,
        "white_gpa_mean":   3.90, "white_gpa_std": 0.22,
        "asian_gpa_mean":   3.80, "asian_gpa_std": 0.15,
        "white_sat_mean":   1350, "white_sat_std": 119,
        "asian_sat_mean":   1400, "asian_sat_std": 119,
        "white_admit_rate": 0.620,
        "asian_admit_rate": 0.540,
    },

    # ================================================================
    # HARVARD — Classes of 2000–2017 (DX042, SFFA v. Harvard)
    #
    # Proportions: Asian Am % of Apps and White % of Apps from DX042.0001-0003
    # Admit rates: Admits/Apps computed from DX042 raw counts
    # SAT means: DX042.0010-0011 section averages × 2 (1600-scale conversion)
    # GPA: estimated from Arcidiacono et al. (2022) litigation data
    # ================================================================
    {
        "label":            "Harvard Class of 2000",
        # DX042: Asian Apps=3683 (20.3%), Admits=340; White Apps=6991 (38.4%), Admits=863; Total=18183
        "total_applicants": 18183,
        "white_proportion": 0.384,
        "asian_proportion": 0.203,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=717, White=703 → ×2
        "white_sat_mean":   1406, "white_sat_std": 140,
        "asian_sat_mean":   1434, "asian_sat_std": 130,
        "white_admit_rate": round(863/6991, 4),   # 12.34%
        "asian_admit_rate": round(340/3683, 4),   # 9.23%
    },
    {
        "label":            "Harvard Class of 2001",
        # DX042: Asian Apps=3314 (20.0%), Admits=367; White Apps=6138 (37.0%), Admits=867; Total=16597
        "total_applicants": 16597,
        "white_proportion": 0.370,
        "asian_proportion": 0.200,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=718, White=701 → ×2
        "white_sat_mean":   1402, "white_sat_std": 140,
        "asian_sat_mean":   1436, "asian_sat_std": 130,
        "white_admit_rate": round(867/6138, 4),   # 14.13%
        "asian_admit_rate": round(367/3314, 4),   # 11.07%
    },
    {
        "label":            "Harvard Class of 2002",
        # DX042: Asian Apps=3321 (19.7%), Admits=375; White Apps=6587 (39.2%), Admits=912; Total=16818
        "total_applicants": 16818,
        "white_proportion": 0.392,
        "asian_proportion": 0.197,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=720, White=708 → ×2
        "white_sat_mean":   1416, "white_sat_std": 140,
        "asian_sat_mean":   1440, "asian_sat_std": 130,
        "white_admit_rate": round(912/6587, 4),   # 13.84%
        "asian_admit_rate": round(375/3321, 4),   # 11.29%
    },
    {
        "label":            "Harvard Class of 2003",
        # DX042: Asian Apps=3537 (19.5%), Admits=339; White Apps=7652 (42.1%), Admits=997; Total=18161
        "total_applicants": 18161,
        "white_proportion": 0.421,
        "asian_proportion": 0.195,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=723, White=711 → ×2
        "white_sat_mean":   1422, "white_sat_std": 140,
        "asian_sat_mean":   1446, "asian_sat_std": 130,
        "white_admit_rate": round(997/7652, 4),   # 13.03%
        "asian_admit_rate": round(339/3537, 4),   # 9.58%
    },
    {
        "label":            "Harvard Class of 2004",
        # DX042: Asian Apps=3637 (19.5%), Admits=332; White Apps=7372 (39.4%), Admits=968; Total=18693
        "total_applicants": 18693,
        "white_proportion": 0.394,
        "asian_proportion": 0.195,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=724, White=711 → ×2
        "white_sat_mean":   1422, "white_sat_std": 140,
        "asian_sat_mean":   1448, "asian_sat_std": 130,
        "white_admit_rate": round(968/7372, 4),   # 13.13%
        "asian_admit_rate": round(332/3637, 4),   # 9.13%
    },
    {
        "label":            "Harvard Class of 2005",
        # DX042: Asian Apps=3736 (19.6%), Admits=297; White Apps=7420 (39.0%), Admits=969; Total=19014
        "total_applicants": 19014,
        "white_proportion": 0.390,
        "asian_proportion": 0.196,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=720, White=710 → ×2
        "white_sat_mean":   1420, "white_sat_std": 140,
        "asian_sat_mean":   1440, "asian_sat_std": 130,
        "white_admit_rate": round(969/7420, 4),   # 13.06%
        "asian_admit_rate": round(297/3736, 4),   # 7.95%
    },
    {
        "label":            "Harvard Class of 2006",
        # DX042: Asian Apps=4022 (20.5%), Admits=340; White Apps=8643 (44.1%), Admits=1055; Total=19608
        "total_applicants": 19608,
        "white_proportion": 0.441,
        "asian_proportion": 0.205,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=721, White=712 → ×2
        "white_sat_mean":   1424, "white_sat_std": 140,
        "asian_sat_mean":   1442, "asian_sat_std": 130,
        "white_admit_rate": round(1055/8643, 4),  # 12.21%
        "asian_admit_rate": round(340/4022, 4),   # 8.45%
    },
    {
        "label":            "Harvard Class of 2007",
        # DX042: Asian Apps=4459 (21.2%), Admits=339; White Apps=8974 (42.8%), Admits=1049; Total=20987
        "total_applicants": 20987,
        "white_proportion": 0.428,
        "asian_proportion": 0.212,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=727, White=718 → ×2
        "white_sat_mean":   1436, "white_sat_std": 140,
        "asian_sat_mean":   1454, "asian_sat_std": 130,
        "white_admit_rate": round(1049/8974, 4),  # 11.69%
        "asian_admit_rate": round(339/4459, 4),   # 7.60%
    },
    {
        "label":            "Harvard Class of 2008",
        # DX042: Asian Apps=4290 (21.7%), Admits=403; White Apps=8195 (41.5%), Admits=994; Total=19752
        "total_applicants": 19752,
        "white_proportion": 0.415,
        "asian_proportion": 0.217,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=730, White=720 → ×2
        "white_sat_mean":   1440, "white_sat_std": 140,
        "asian_sat_mean":   1460, "asian_sat_std": 130,
        "white_admit_rate": round(994/8195, 4),   # 12.13%
        "asian_admit_rate": round(403/4290, 4),   # 9.39%
    },
    {
        "label":            "Harvard Class of 2009",
        # DX042: Asian Apps=4804 (21.1%), Admits=371; White Apps=8492 (37.3%), Admits=957; Total=22796
        "total_applicants": 22796,
        "white_proportion": 0.373,
        "asian_proportion": 0.211,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=730, White=718 → ×2
        "white_sat_mean":   1436, "white_sat_std": 140,
        "asian_sat_mean":   1460, "asian_sat_std": 130,
        "white_admit_rate": round(957/8492, 4),   # 11.27%
        "asian_admit_rate": round(371/4804, 4),   # 7.72%
    },
    {
        "label":            "Harvard Class of 2010",
        # DX042: Asian Apps=4865 (21.4%), Admits=375; White Apps=7761 (34.1%), Admits=899; Total=22754
        "total_applicants": 22754,
        "white_proportion": 0.341,
        "asian_proportion": 0.214,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=727, White=712 → ×2
        "white_sat_mean":   1424, "white_sat_std": 140,
        "asian_sat_mean":   1454, "asian_sat_std": 130,
        "white_admit_rate": round(899/7761, 4),   # 11.58%
        "asian_admit_rate": round(375/4865, 4),   # 7.71%
    },
    {
        "label":            "Harvard Class of 2011",
        # DX042: Asian Apps=4803 (20.9%), Admits=411; White Apps=7659 (33.4%), Admits=838; Total=22955
        "total_applicants": 22955,
        "white_proportion": 0.334,
        "asian_proportion": 0.209,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=728, White=712 → ×2
        "white_sat_mean":   1424, "white_sat_std": 140,
        "asian_sat_mean":   1456, "asian_sat_std": 130,
        "white_admit_rate": round(838/7659, 4),   # 10.94%
        "asian_admit_rate": round(411/4803, 4),   # 8.56%
    },
    {
        "label":            "Harvard Class of 2012",
        # DX042: Asian Apps=5378 (19.6%), Admits=415; White Apps=8594 (31.3%), Admits=853; Total=27462
        "total_applicants": 27462,
        "white_proportion": 0.313,
        "asian_proportion": 0.196,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=726, White=713 → ×2
        "white_sat_mean":   1426, "white_sat_std": 140,
        "asian_sat_mean":   1452, "asian_sat_std": 130,
        "white_admit_rate": round(853/8594, 4),   # 9.93%
        "asian_admit_rate": round(415/5378, 4),   # 7.72%
    },
    {
        "label":            "Harvard Class of 2013",
        # DX042: Asian Apps=5784 (19.9%), Admits=380; White Apps=9190 (31.6%), Admits=837; Total=29114
        "total_applicants": 29114,
        "white_proportion": 0.316,
        "asian_proportion": 0.199,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.25,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.20,
        # DX042 SAT section avg: Asian=730, White=715 → ×2
        "white_sat_mean":   1430, "white_sat_std": 140,
        "asian_sat_mean":   1460, "asian_sat_std": 130,
        "white_admit_rate": round(837/9190, 4),   # 9.11%
        "asian_admit_rate": round(380/5784, 4),   # 6.57%
    },
    {
        "label":            "Harvard Class of 2014",
        # DX042.0014 (New Meth NLNA): Asian Apps=6449 (21.2%), Admits=394; White Apps=13202 (43.3%), Admits=1052; Total=30489
        "total_applicants": 30489,
        "white_proportion": 0.433,
        "asian_proportion": 0.212,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.24,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.19,
        # DX042.0016 SAT section avg (New Meth): Asian=731, White=712 → ×2
        "white_sat_mean":   1424, "white_sat_std": 140,
        "asian_sat_mean":   1462, "asian_sat_std": 130,
        "white_admit_rate": round(1052/13202, 4), # 7.97%
        "asian_admit_rate": round(394/6449, 4),   # 6.11%
    },
    {
        "label":            "Harvard Class of 2015",
        # DX042.0014: Asian Apps=7310 (20.9%), Admits=385; White Apps=14895 (42.6%), Admits=1082; Total=34950
        "total_applicants": 34950,
        "white_proportion": 0.426,
        "asian_proportion": 0.209,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.24,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.19,
        # DX042.0016 SAT section avg (New Meth): Asian=728, White=707 → ×2
        "white_sat_mean":   1414, "white_sat_std": 140,
        "asian_sat_mean":   1456, "asian_sat_std": 130,
        "white_admit_rate": round(1082/14895, 4), # 7.27%
        "asian_admit_rate": round(385/7310, 4),   # 5.27%
    },
    {
        "label":            "Harvard Class of 2016",
        # DX042.0014: Asian Apps=7011 (20.4%), Admits=422; White Apps=11346 (33.1%), Admits=851; Total=34303
        "total_applicants": 34303,
        "white_proportion": 0.331,
        "asian_proportion": 0.204,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.24,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.19,
        # DX042.0016 SAT section avg (New Meth): Asian=733, White=713 → ×2
        "white_sat_mean":   1426, "white_sat_std": 138,
        "asian_sat_mean":   1466, "asian_sat_std": 128,
        "white_admit_rate": round(851/11346, 4),  # 7.50%
        "asian_admit_rate": round(422/7011, 4),   # 6.02%
    },
    {
        "label":            "Harvard Class of 2017",
        # DX042.0015: Asian Apps=7133 (20.7%), Admits=400; White Apps=11415 (32.6% from page 3), Admits=794; Total=35023
        "total_applicants": 35023,
        "white_proportion": 0.326,
        "asian_proportion": 0.207,
        "white_gpa_mean":   3.85, "white_gpa_std": 0.24,
        "asian_gpa_mean":   3.89, "asian_gpa_std": 0.19,
        # DX042.0016 SAT section avg (New Meth): Asian=733, White=717 → ×2
        "white_sat_mean":   1434, "white_sat_std": 138,
        "asian_sat_mean":   1466, "asian_sat_std": 128,
        "white_admit_rate": round(794/11415, 4),  # 6.96%
        "asian_admit_rate": round(400/7133, 4),   # 5.61%
    },

    # ---- ADD NEW DATASETS BELOW THIS LINE ----
    # {
    #     "label":            "My University YYYY",
    #     "total_applicants": 30000,
    #     "white_proportion": 0.55,   # independent of asian_proportion
    #     "asian_proportion": 0.20,   # white + asian do NOT need to sum to 1
    #     "white_gpa_mean":   3.80, "white_gpa_std": 0.22,
    #     "asian_gpa_mean":   3.85, "asian_gpa_std": 0.15,
    #     "white_sat_mean":   1320, "white_sat_std": 120,
    #     "asian_sat_mean":   1400, "asian_sat_std": 110,
    #     "white_admit_rate": 0.15,
    #     "asian_admit_rate": 0.10,
    # },
]