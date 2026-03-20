from fpdf import FPDF

def generate_pdf_bytes(title, data_dict, ai_result):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt=title.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.ln(10)
    
    # Input Data
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Input Data:", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in data_dict.items():
        safe_k = str(k).encode('latin-1', 'replace').decode('latin-1')
        safe_v = str(v).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 8, txt=f"{safe_k}: {safe_v}", ln=True)
    
    pdf.ln(10)
    
    # AI Report
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="AI Analysis Report:", ln=True)
    pdf.set_font("Arial", size=11)
    
    safe_text = str(ai_result).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=safe_text)
    
    # Return as bytes
    result = pdf.output(dest='S')
    if isinstance(result, str):
        return result.encode('latin-1')
    return bytes(result)
