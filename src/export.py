from fpdf import FPDF
import io
import pandas as pd
import os

def generate_pdf(df: pd.DataFrame) -> io.BytesIO:
    """
    Generate a one-page PDF report containing prediction results.

    This function creates a simple tabular PDF that summarizes the latest 
    prediction row(s) from a given DataFrame. It uses the `fpdf` library 
    with a Unicode-compatible font (DejaVu Sans) to support a wide range 
    of characters.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing prediction results. Each row represents 
        a prediction session, and each column represents an attribute 
        (e.g., patient info, staging, risk level, etc.).

    Returns
    -------
    io.BytesIO
        An in-memory byte stream of the generated PDF.
        
    """
    pdf = FPDF()
    pdf.add_page()
    
    font_path = os.path.join(os.path.dirname(__file__), os.pardir, "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    
    pdf.set_fill_color(224, 235, 255)
    pdf.set_text_color(40, 40, 40)

    pdf.cell(200, 10, txt="Thyroid Cancer Prediction Report", ln=True, align='C')
    pdf.ln(10)

    # --- PDF header ---
    for col in df.columns:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()
    
    # --- Table rows ---
    for _, row in df.iterrows():
        for col in df.columns:
            pdf.cell(40, 10, str(row[col]), border=1)
        pdf.ln()
    

    pdf_bytes = pdf.output(dest='S')
    return io.BytesIO(pdf_bytes)
