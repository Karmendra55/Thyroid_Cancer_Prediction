import streamlit as st
import numpy as np

# --- Encoders ---
GENDER_MAP = {"F": 0, "M": 1}
YN_MAP = {"No": 0, "Yes": 1}
THYROID_FUNC_MAP = {
    "Euthyroid": 0, "Clinical Hyperthyroidism": 1, "Clinical Hypothyroidism": 2,
    "Subclinical Hyperthyroidism": 3, "Subclinical Hypothyroidism": 4
}
PHYSICAL_EXAM_MAP = {
    "Single nodular goiter-left": 0, "Multinodular goiter": 1,
    "Single nodular goiter-right": 2, "Normal": 3, "Diffuse goiter": 4
}
ADENOPATHY_MAP = {"No": 0, "Right": 1, "Extensive": 2, "Left": 3, "Bilateral": 4, "Posterior": 5}
PATHOLOGY_MAP = {"Micropapillary": 0, "Papillary": 1, "Follicular": 2, "Hurthel cell": 3}
FOCALITY_MAP = {"Uni-Focal": 0, "Multi-Focal": 1}
RISK_MAP = {"Low": 0, "Intermediate": 1, "High": 2}
T_MAP = {"T1a": 0, "T1b": 1, "T2": 2, "T3a": 3, "T3b": 4, "T4a": 5, "T4b": 6}
N_MAP = {"N0": 0, "N1b": 1, "N1a": 2}
M_MAP = {"M0": 0, "M1": 1}
STAGE_MAP = {"I": 0, "II": 1, "III": 2, "IVA": 3, "IVB": 4}
RESPONSE_MAP = {"Indeterminate": 0, "Excellent": 1, "Structural Incomplete": 2, "Biochemical Incomplete": 3}

def _encode(val, mapping): 
    """
    Encode a categorical value into its corresponding numeric code.

    Parameters
    ----------
    val : str
        The categorical input value (e.g., "F", "Yes", "Papillary").
        Must exist as a key in the provided mapping dictionary.
    mapping : dict
        A dictionary that maps categorical string values to integer codes.
        Example:
            {"F": 0, "M": 1}

    Returns
    -------
    int
        The integer code corresponding to the given categorical value.
        
    """
    return mapping[val]

def render_input_form():
    """
    Render a patient input form and return encoded data, raw values, 
    and narration preferences.

    This function builds a multi-column Streamlit form for collecting 
    patient demographics, clinical history, staging information, 
    pathology, risk factors, and treatment response. It supports demo 
    mode (via ``st.session_state['use_demo']``).

    Returns
    -------
    dict[str, object]
        A dictionary with three keys:
        
        - ``"input_array"`` : np.ndarray        
        - ``"raw"`` : dict[str, str | int]
        - ``"narration"`` : dict[str, str | bool]
 
    Behavior
    --------
    - Renders multiple columns of input fields (text, number, select boxes, checkboxes).
    - Encodes categorical variables using mapping dictionaries 
      (e.g., ``GENDER_MAP``, ``YN_MAP``).
    - Ensures feature order matches the ML model's training pipeline.
    - Provides an expander for narration settings with language/voice options.

    """
    demo_data = st.session_state.demo_data if st.session_state.get("use_demo") else {}
    tab1, tab2 = st.columns([2,1])
    tab3, tab4, tab5, tab6 = st.columns([1,1,1,1])
    tab7, tab8, tab9= st.columns([1,1,1])
    with tab1:
        name = st.text_input("Patient Name (optional)", help="Enter patient's first name (optional).",
                         value=demo_data.get("name", ""))
    with tab2:
        age = st.number_input("Age", min_value=1, max_value=100,
                          help="Patient's age in years.", value=demo_data.get("age", 25))
    with tab3:
        gender = st.selectbox("Gender", ["F", "M"],
                          help="Biological sex of the patient.",
                          index=["F", "M"].index(demo_data.get("gender", "F")))

    with tab4:   
        smoking = st.selectbox("Smoking", ["No", "Yes"], help="Does the patient currently smoke?",
                           index=["No", "Yes"].index(demo_data.get("smoking", "No")))
    with tab5:    
        hx_smoking = st.selectbox("History of Smoking", ["No", "Yes"],
                              help="Past history of smoking.",
                              index=["No", "Yes"].index(demo_data.get("hx_smoking", "No")))
    with tab6:
        hx_radiotherapy = st.selectbox("History Radiotherapy", ["No", "Yes"],
                                   help="Any previous radiation therapy?",
                                   index=["No", "Yes"].index(demo_data.get("hx_radiotherapy", "No")))

    with tab7:
        thyroid_func_opts = list(THYROID_FUNC_MAP.keys())
        thyroid_func = st.selectbox("Thyroid Function", thyroid_func_opts,
                                help="Current thyroid hormone status.",
                                index=thyroid_func_opts.index(demo_data.get("thyroid_func", "Euthyroid")))
        pathology_opts = list(PATHOLOGY_MAP.keys())
        pathology = st.selectbox("Pathology", pathology_opts,
                             help="Type of thyroid tumor found on biopsy.",
                             index=pathology_opts.index(demo_data.get("pathology", "Papillary")))
    with tab8:
        physical_exam_opts = list(PHYSICAL_EXAM_MAP.keys())
        physical_exam = st.selectbox("Physical Examination", physical_exam_opts,
                                 help="Doctor's physical exam findings.",
                                 index=physical_exam_opts.index(demo_data.get("physical_exam", "Normal")))
        focality_opts = list(FOCALITY_MAP.keys())
        focality = st.selectbox("Focality", focality_opts, help="Number of cancerous nodules.",
                            index=focality_opts.index(demo_data.get("focality", "Uni-Focal")))

    with tab9:
        adenopathy_opts = list(ADENOPATHY_MAP.keys())
        adenopathy = st.selectbox("Adenopathy", adenopathy_opts, help="Lymph node involvement.",
                              index=adenopathy_opts.index(demo_data.get("adenopathy", "No")))
        risk_opts = list(RISK_MAP.keys())
        risk = st.selectbox("Risk Level", risk_opts, help="Clinically assessed risk level.",
                        index=risk_opts.index(demo_data.get("risk", "Low")))
    
    with tab3:
        T_opts = list(T_MAP.keys())
        T = st.selectbox("T (Tumor)", T_opts, help="Tumor staging (size/extent).",
                     index=T_opts.index(demo_data.get("T", "T1a")))
    with tab4:
        N_opts = list(N_MAP.keys())
        N = st.selectbox("N (Nodes)", N_opts, help="Lymph node staging.",
                     index=N_opts.index(demo_data.get("N", "N0")))
    with tab5:
        M_opts = list(M_MAP.keys())
        M = st.selectbox("M (Metastasis)", M_opts, help="Metastasis present?",
                     index=M_opts.index(demo_data.get("M", "M0")))
    with tab6:
        stage_opts = list(STAGE_MAP.keys())
        stage = st.selectbox("Stage", stage_opts, help="Overall cancer stage.",
                         index=stage_opts.index(demo_data.get("stage", "I")))

    response_opts = list(RESPONSE_MAP.keys())
    response = st.selectbox("Response to Treatment", response_opts,
                            help="How well the patient responded to previous treatment.",
                            index=response_opts.index(demo_data.get("response", "Excellent")))

    with st.expander("🔈 Narration Settings"):
        narration_lang = st.selectbox("Language", ["English", "Hindi"])
        if narration_lang == "English":
            narration_voice = st.selectbox("Voice Type", ["Male", "Female"])
        else:
            narration_voice = "Female"
            st.markdown(
                "<span style='color: gray; font-size: 0.9em;'>Note: Only a female voice is available for Hindi narration.</span>",
                unsafe_allow_html=True
            )
    narrate = st.checkbox("🔊 Narrate Prediction")

    encoded_row = [
        age,
        _encode(gender, GENDER_MAP),
        _encode(smoking, YN_MAP),
        _encode(hx_smoking, YN_MAP),
        _encode(hx_radiotherapy, YN_MAP),
        _encode(thyroid_func, THYROID_FUNC_MAP),
        _encode(physical_exam, PHYSICAL_EXAM_MAP),
        _encode(adenopathy, ADENOPATHY_MAP),
        _encode(pathology, PATHOLOGY_MAP),
        _encode(focality, FOCALITY_MAP),
        _encode(risk, RISK_MAP),
        _encode(T, T_MAP),
        _encode(N, N_MAP),
        _encode(M, M_MAP),
        _encode(stage, STAGE_MAP),
        _encode(response, RESPONSE_MAP)
    ]

    input_array = np.array([encoded_row])

    return {
        "input_array": input_array,
        "raw": {
            "name": name, "age": age, "gender": gender, "smoking": smoking, "hx_smoking": hx_smoking,
            "hx_radiotherapy": hx_radiotherapy, "thyroid_func": thyroid_func, "physical_exam": physical_exam,
            "adenopathy": adenopathy, "pathology": pathology, "focality": focality, "risk": risk,
            "T": T, "N": N, "M": M, "stage": stage, "response": response
        },
        "narration": {"enabled": narrate, "lang": narration_lang, "voice": narration_voice}
    }
