import random

def generate_demo_data(counter=1):
    return {
        "name": f"Demo Patient {counter}",
        "age": random.randint(1, 100),
        "gender": random.choice(["F", "M"]),
        "smoking": random.choice(["Yes", "No"]),
        "hx_smoking": random.choice(["Yes", "No"]),
        "hx_radiotherapy": random.choice(["Yes", "No"]),
        "thyroid_func": random.choice([
            "Euthyroid", "Clinical Hyperthyroidism", "Clinical Hypothyroidism",
            "Subclinical Hyperthyroidism", "Subclinical Hypothyroidism"
        ]),
        "physical_exam": random.choice([
            "Single nodular goiter-left", "Multinodular goiter",
            "Single nodular goiter-right", "Normal", "Diffuse goiter"
        ]),
        "adenopathy": random.choice([
            "No", "Right", "Extensive", "Left", "Bilateral", "Posterior"
        ]),
        "pathology": random.choice([
            "Micropapillary", "Papillary", "Follicular", "Hurthel cell"
        ]),
        "focality": random.choice(["Uni-Focal", "Multi-Focal"]),
        "risk": random.choice(["Low", "Intermediate", "High"]),
        "T": random.choice(["T1a", "T1b", "T2", "T3a", "T3b", "T4a", "T4b"]),
        "N": random.choice(["N0", "N1b", "N1a"]),
        "M": random.choice(["M0", "M1"]),
        "stage": random.choice(["I", "II", "III", "IVA", "IVB"]),
        "response": random.choice([
            "Indeterminate", "Excellent", "Structural Incomplete", "Biochemical Incomplete"
        ])
    }
