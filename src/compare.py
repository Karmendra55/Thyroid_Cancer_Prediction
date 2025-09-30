import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_comparison(history):
    if not history:
        st.info("No patients to compare yet.")
        return

    st.markdown("## 📊 Patient Comparison Dashboard")

    df = pd.DataFrame(history)

    st.markdown("### 🧾 Patient Summary Table")
    st.dataframe(df)

    # Sort by Recurrence Confidence
    st.markdown("### 🔥 Top Risk Patients")
    top_patients = df.sort_values(by="Confidence_Yes", ascending=False).head(5)
    st.dataframe(top_patients)

    # Confidence Distribution
    st.markdown("### 📈 Confidence Distribution")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=df, x="Name", y="Confidence_Yes", palette="Reds_r", ax=ax1, ci=None)
    ax1.set_ylabel("Recurrence Confidence")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30, ha='right')
    st.pyplot(fig1)

    # Risk Category Overview
    st.markdown("### ⚠️ Risk Category Breakdown")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x="Risk", hue="Prediction", palette="muted", ax=ax2)
    st.pyplot(fig2)

    # Recurrence Outcome Pie
    st.markdown("### 🔍 Prediction Split")
    fig3, ax3 = plt.subplots()
    outcome_counts = df['Prediction'].value_counts()
    ax3.pie(outcome_counts, labels=outcome_counts.index, autopct='%1.1f%%', startangle=140)
    ax3.axis('equal')
    st.pyplot(fig3)
