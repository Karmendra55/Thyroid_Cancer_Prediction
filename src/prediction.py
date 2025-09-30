import os
import uuid
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st

from utils import narration as narration_util

@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load the trained thyroid cancer recurrence prediction model.

    This function loads a serialized scikit-learn model and its associated 
    feature names from disk. For convenience, it also re-saves only the 
    classifier object to a separate file.

    Returns
    -------
    tuple
        clf : sklearn.base.BaseEstimator
            The trained classifier (RandomForest or similar).
        feature_names : list of str
            Names of the features used during training.
    """
    clf, feature_names = joblib.load("trained_model/thyroid_recurrence_rf.pkl")
    joblib.dump(clf, "trained_model/thyroid_recurrence_rf_only.pkl")
    return clf, feature_names

def _is_high_risk(stage_str: str, m_str: str) -> int:
    """
    Determine if a patient is classified as high-risk.

    A patient is considered high-risk if:
    - Their stage is IVA or IVB, OR
    - They have distant metastasis (M1).

    Parameters
    ----------
    stage_str : str
        The cancer stage (e.g., "I", "II", "III", "IVA", "IVB").
    m_str : str
        The metastasis status ("M0" or "M1").

    Returns
    -------
    int
        1 if the patient is high-risk, otherwise 0.
    """
    return 1 if (stage_str in ["IVA", "IVB"] or m_str == "M1") else 0

def _save_history_to_csv(history_rows):
    """
    Save session history to a timestamped CSV file.

    This function stores model input/output history for the current session 
    in the `output/sessions/` directory. Each saved file is uniquely named 
    with the current date and time.

    Parameters
    ----------
    history_rows : list of dict
        A list of records (rows), where each record is a dictionary 
        mapping column names to values. Each row represents one 
        prediction session.

    Args:
        history_rows (_type_): _description_
    """
    if not history_rows:
        return
    history_dir = "output/sessions"
    os.makedirs(history_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    session_file = os.path.join(history_dir, f"session_{timestamp}.csv")
    pd.DataFrame(history_rows).to_csv(session_file, index=False)

def run_prediction(inputs: dict):
    """
    Run recurrence prediction, display results, and update session history.

    This function loads the trained model, makes predictions based on the 
    encoded patient input, evaluates recurrence risk, and presents results 
    interactively within the Streamlit app. It also logs predictions into 
    session history and optionally narrates results if narration is enabled.

    Parameters
    ----------
    inputs : dict

    Behavior
    --------
    - Renders a **Predict** button in the Streamlit UI.
    - When clicked:
        * Computes recurrence probabilities via ``model.predict_proba``.
        * Displays prediction and model confidence values.
        * Issues a warning if the result is borderline.
        * Updates ``st.session_state.history`` with a structured row.
        * Saves updated history to CSV via ``_save_history_to_csv``.
        * Optionally narrates results using ``narration_util.narrate_result``.

    Returns
    -------
    None
        This function does not return a value. Results are displayed in 
        the UI and stored in session state/history.
        
    """
    model, feature_names = load_model()
    input_array = inputs["input_array"]
    raw = inputs["raw"]
    narration = inputs["narration"]

    if st.button("Predict"):
        proba = model.predict_proba(input_array)[0]
        conf_no, conf_yes = float(proba[0]), float(proba[1])

        high_risk = _is_high_risk(raw["stage"], raw["M"])

        # --- Decision thresholds ---
        if conf_yes >= 0.5 or (conf_yes >= 0.35 and high_risk == 1):
            result = "✔️ Recurrence Likely"
            result_code = 0
        elif 0.30 < conf_yes < 0.50:
            st.warning("⚠️ Borderline case: Please consider further testing and specialist evaluation.")
            result = "⚠️ Borderline"
            result_code = 1
        else:
            result = "❌ No Recurrence Expected"
            result_code = 2

        st.success(f"Prediction: {result}")
        st.write(f"🔍 Model Confidence → No Recurrence: {conf_no:.2f} | Recurrence: {conf_yes:.2f}")

        # --- Append to session history ---
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_id = str(uuid.uuid4())[:8]
        row = {
            "Session ID": session_id,
            "Timestamp": timestamp,
            "Name": raw["name"] if raw["name"] else f"Patient {len(st.session_state.history)+1}",
            "Confidence_No": round(conf_no, 2),
            "Confidence_Yes": round(conf_yes, 2),
            "Prediction": result,
            "Risk": raw["risk"],
            "HighRisk": high_risk,
        }
        st.session_state.history.append(row)

        if narration.get("enabled"):
            result = result.replace("✔️", "").replace("⚠️", "").replace("❌", "").strip()
            narration_util.narrate_result(
                result=result,
                confidence_yes=conf_yes,
                confidence_no=conf_no,
                name=raw["name"],
                language=narration.get("lang", "English"),
                gender=narration.get("voice", "Female")
            )

        _save_history_to_csv(st.session_state.history)
