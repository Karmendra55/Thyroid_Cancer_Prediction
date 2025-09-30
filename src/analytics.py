import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from src import export
from src import compare as compare_module 

def _list_past_session_files():
    """
    List all previously saved session history files.

    This function ensures the `output/sessions/` directory exists and 
    returns the names of all CSV files inside it. Each file typically 
    corresponds to one past prediction session saved with a timestamp.

    Returns
    -------
    list of str
        A list of filenames (not full paths) of CSV files found in 
        `output/sessions/`.
        
    """
    history_dir = "output/sessions"
    os.makedirs(history_dir, exist_ok=True)
    return [f for f in os.listdir(history_dir) if f.endswith(".csv")]

def show_analytics():
    """
    Display analytics and visualizations for prediction history.

    This function provides an interactive analytics dashboard in 
    the Streamlit app, allowing users to review the current session’s 
    predictions, compare them with past session files, and download 
    reports in CSV or PDF format. It also generates charts to 
    visualize prediction confidence, distribution, and risk categories.

    Behavior
    --------
    - Displays the current prediction history stored in 
      st.session_state.history.
    - Allows users to select a past session file for comparison:
        * Computes and displays the delta in mean recurrence confidence.
        * Plots kernel density distributions of recurrence confidence.
    - Provides downloads:
        * Full history as CSV.
        * Latest report as PDF (via ``export.generate_pdf``).
    - Optionally calls ``compare_module.display_comparison`` 
      if available for extended comparisons.
    - Generates the following visualizations for current session data:
        * Confidence scores over prediction index (line chart).
        * Prediction outcome distribution (countplot).
        * Risk category overview (countplot).

    Returns
    -------
    None
        The function does not return a value. It renders UI components 
        and charts in the Streamlit app.
    """
    st.markdown("### Prediction History")

    history = st.session_state.get("history", [])
    history_dir = "output/sessions"
    past_files = _list_past_session_files()

    compare_file = st.selectbox("📂 Compare with Past Session", ["None"] + past_files)

    # --- Comparison ---
    if compare_file != "None":
        prev_df = pd.read_csv(os.path.join(history_dir, compare_file))
        st.markdown(f"### 📊 Comparing with: `{compare_file}`")

        if history:
            current_df = pd.DataFrame(history)

            prev_rec = prev_df["Confidence_Yes"].mean() if not prev_df.empty else 0.0
            curr_rec = current_df["Confidence_Yes"].mean() if not current_df.empty else 0.0
            delta = curr_rec - prev_rec
            st.metric("Avg Recurrence Confidence (Current)", f"{curr_rec:.2f}", delta=f"{delta:.2f}")

            st.markdown("#### 🔍 Recurrence Distribution")
            fig, ax = plt.subplots()
            if "Confidence_Yes" in prev_df.columns:
                sns.kdeplot(prev_df["Confidence_Yes"], label="Previous", fill=True, ax=ax)
            if "Confidence_Yes" in current_df.columns:
                sns.kdeplot(current_df["Confidence_Yes"], label="Current", fill=True, ax=ax)
            ax.legend()
            st.pyplot(fig)

    # --- Current session table + downloads + charts ---
    if history:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True)

        # Downloads
        csv_bytes = df.to_csv(index=False).encode()
        st.download_button("Download Full History (CSV)", csv_bytes, "thyroid_prediction_history.csv", "text/csv")

        pdf_filelike = export.generate_pdf(df) 
        st.download_button("Download Latest Report (PDF)", data=pdf_filelike,
                           file_name="prediction_report.pdf", mime="application/pdf")

        st.markdown("---")
        
        if hasattr(compare_module, "display_comparison"):
            compare_module.display_comparison(history)

        # --- Charts
        st.markdown("### Confidence Over Time")
        fig1, ax1 = plt.subplots()
        df.reset_index().rename(columns={"index": "Prediction Index"}).plot(
            kind='line', x="Prediction Index", y=["Confidence_Yes", "Confidence_No"], ax=ax1, marker='o'
        )
        ax1.set_xlabel("Prediction Index")
        ax1.set_ylabel("Confidence")
        st.pyplot(fig1)

        st.markdown("### Recurrence Prediction Breakdown")
        fig2, ax2 = plt.subplots()
        sns.countplot(data=df, x='Prediction', ax=ax2, palette='pastel')
        st.pyplot(fig2)

        st.markdown("### Risk Category Overview")
        fig3, ax3 = plt.subplots()
        sns.countplot(data=df, x='Risk', ax=ax3, palette='muted')
        st.pyplot(fig3)

    else:
        st.info("No predictions made yet.")
