import streamlit as st
from datetime import datetime
from components.health_score import extract_health_metrics, calculate_health_score, get_score_color

def generate_pdf_html(patient_name, age, gender, analysis_text, score, score_label, score_color, metrics):
    """Generate clean HTML for PDF conversion."""
    
    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%H:%M")

    # Build metrics table rows
    metrics_rows = ""
    if metrics:
        for metric, status in metrics.items():
            if status == "normal":
                color = "#68D391"
                label = "✓ Normal"
                bg = "rgba(104, 211, 145, 0.1)"
            elif status == "warning":
                color = "#F6AD55"
                label = "⚠ Borderline"
                bg = "rgba(246, 173, 85, 0.1)"
            else:
                color = "#FC8181"
                label = "✗ Critical"
                bg = "rgba(252, 129, 129, 0.1)"

            metrics_rows += f"""
                <tr>
                    <td style="padding: 0.6rem 1rem; color: #CBD5E0; border-bottom: 1px solid #2D3748;">{metric}</td>
                    <td style="padding: 0.6rem 1rem; border-bottom: 1px solid #2D3748;">
                        <span style="
                            color: {color};
                            background: {bg};
                            padding: 0.2rem 0.75rem;
                            border-radius: 20px;
                            font-size: 0.85rem;
                            font-weight: 600;
                        ">{label}</span>
                    </td>
                </tr>
            """
    else:
        metrics_rows = """
            <tr>
                <td colspan="2" style="padding: 1rem; color: #64748B; text-align: center;">
                    No specific markers detected
                </td>
            </tr>
        """

    # Format analysis text
    formatted_analysis = analysis_text.replace('\n', '<br/>')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #0F172A;
                color: #F1F5F9;
                padding: 2rem;
                line-height: 1.6;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 1.5rem;
                border-bottom: 1px solid #2D3748;
                margin-bottom: 2rem;
            }}
            .logo {{
                font-size: 1.5rem;
                font-weight: 700;
                color: #63B3ED;
                letter-spacing: -0.02em;
            }}
            .date {{
                color: #64748B;
                font-size: 0.85rem;
            }}
            .patient-card {{
                background: #1E293B;
                border: 1px solid #2D3748;
                border-radius: 12px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1.5rem;
                display: flex;
                gap: 2rem;
            }}
            .patient-field {{
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }}
            .field-label {{
                color: #64748B;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}
            .field-value {{
                color: #F1F5F9;
                font-size: 1rem;
                font-weight: 500;
            }}
            .score-section {{
                background: #1E293B;
                border: 1px solid #2D3748;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                text-align: center;
            }}
            .score-number {{
                font-size: 4rem;
                font-weight: 700;
                color: {score_color};
                line-height: 1;
            }}
            .score-label {{
                color: {score_color};
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 0.5rem;
            }}
            .score-sub {{
                color: #64748B;
                font-size: 0.85rem;
                margin-top: 0.25rem;
            }}
            .section-title {{
                color: #94A3B8;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
            }}
            .metrics-table {{
                width: 100%;
                border-collapse: collapse;
                background: #1E293B;
                border: 1px solid #2D3748;
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 1.5rem;
            }}
            .analysis-box {{
                background: #1E293B;
                border: 1px solid #2D3748;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                color: #CBD5E0;
                font-size: 0.92rem;
                line-height: 1.8;
            }}
            .disclaimer {{
                color: #334155;
                font-size: 0.75rem;
                text-align: center;
                padding-top: 1rem;
                border-top: 1px solid #1E293B;
            }}
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid #2D3748;
                color: #334155;
                font-size: 0.75rem;
            }}
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <div class="logo">🩺 VitalAI</div>
            <div class="date">Generated on {current_date} at {current_time}</div>
        </div>

        <!-- Patient Info -->
        <p class="section-title">Patient Information</p>
        <div class="patient-card">
            <div class="patient-field">
                <span class="field-label">Name</span>
                <span class="field-value">{patient_name}</span>
            </div>
            <div class="patient-field">
                <span class="field-label">Age</span>
                <span class="field-value">{age} years</span>
            </div>
            <div class="patient-field">
                <span class="field-label">Gender</span>
                <span class="field-value">{gender}</span>
            </div>
            <div class="patient-field">
                <span class="field-label">Report Date</span>
                <span class="field-value">{current_date}</span>
            </div>
        </div>

        <!-- Health Score -->
        <p class="section-title">Overall Health Score</p>
        <div class="score-section">
            <div class="score-number">{score}</div>
            <div class="score-label">{score_label}</div>
            <div class="score-sub">out of 100</div>
        </div>

        <!-- Health Indicators -->
        <p class="section-title">Health Indicators</p>
        <table class="metrics-table">
            <tbody>
                {metrics_rows}
            </tbody>
        </table>

        <!-- Full Analysis -->
        <p class="section-title">AI Analysis</p>
        <div class="analysis-box">
            {formatted_analysis}
        </div>

        <!-- Disclaimer -->
        <p class="disclaimer">
            ⚕️ This report is AI-generated by VitalAI and is not a substitute for professional medical advice.
            Please consult a qualified healthcare provider for diagnosis and treatment.
        </p>

        <!-- Footer -->
        <div class="footer">
            <span>VitalAI — AI-Powered Health Analysis</span>
            <span>github.com/Haneesh-Nellore/VitalAI</span>
        </div>
    </body>
    </html>
    """
    return html


def show_pdf_export_button(patient_name, age, gender, analysis_text):
    """
    Show a download button that exports the analysis as an HTML report.
    The HTML can be opened in browser and printed/saved as PDF.
    """
    if not analysis_text:
        return

    # Calculate health data
    metrics = extract_health_metrics(analysis_text)
    score = calculate_health_score(metrics)
    score_color, score_label = get_score_color(score)

    # Generate HTML report
    html_content = generate_pdf_html(
        patient_name=patient_name,
        age=age,
        gender=gender,
        analysis_text=analysis_text,
        score=score,
        score_label=score_label,
        score_color=score_color,
        metrics=metrics
    )

    # Filename
    safe_name = patient_name.replace(" ", "_").lower()
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"VitalAI_Report_{safe_name}_{date_str}.html"

    st.markdown("""
        <p style='
            color: #64748B;
            font-size: 0.78rem;
            margin: 0.25rem 0 0.75rem 0;
        '>
            💡 Download the report, open it in your browser, and use <b>Ctrl+P → Save as PDF</b>
        </p>
    """, unsafe_allow_html=True)

    st.download_button(
        label="📄 Download Health Report",
        data=html_content,
        file_name=filename,
        mime="text/html",
        use_container_width=True,
        type="primary"
    )
