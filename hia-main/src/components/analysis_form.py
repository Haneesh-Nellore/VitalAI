import streamlit as st
from config.prompts import SPECIALIST_PROMPTS
from utils.pdf_extractor import extract_text_from_pdf
from config.sample_data import SAMPLE_REPORT
from config.app_config import MAX_UPLOAD_SIZE_MB
from components.pdf_export import show_pdf_export_button


def show_analysis_form():
    if "report_source" not in st.session_state:
        st.session_state.report_source = "Upload PDF"

    report_source = st.radio(
        "Choose report source",
        ["Upload PDF", "Use Sample PDF"],
        horizontal=True,
        key="report_source",
    )

    if report_source == "Upload PDF":
        uploaded_file = st.file_uploader(
            f"Upload blood report PDF (Max {MAX_UPLOAD_SIZE_MB}MB)",
            type=["pdf"],
            help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB}MB",
            key="pdf_uploader"
        )

        if uploaded_file is not None:
            # Extract and store in session state
            if st.session_state.get("uploaded_file_name") != uploaded_file.name:
                with st.spinner("Reading PDF..."):
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    if file_size_mb > MAX_UPLOAD_SIZE_MB:
                        st.error(f"File too large ({file_size_mb:.1f}MB).")
                        return

                    try:
                        text = ""
                        import pdfplumber
                        with pdfplumber.open(uploaded_file) as pdf:
                            for page in pdf.pages:
                                extracted = page.extract_text()
                                if extracted:
                                    text += extracted + "\n"

                        if len(text.strip()) < 10:
                            st.error("Could not extract text from this PDF.")
                            return

                        st.session_state.uploaded_pdf_text = text
                        st.session_state.uploaded_file_name = uploaded_file.name
                    except Exception as e:
                        st.error(f"Failed to read PDF: {str(e)}")
                        return

            # PDF is ready — show button
            if st.session_state.get("uploaded_pdf_text"):
                st.success(f"✅ {uploaded_file.name} loaded and ready!")
                if st.button(
                    "🔍 Analyze Report",
                    type="primary",
                    use_container_width=True,
                    key="analyze_btn"
                ):
                    run_analysis(st.session_state.uploaded_pdf_text)

    else:
        # Sample PDF
        st.info("Using built-in sample blood report.")
        if st.button(
            "🔍 Analyze Sample Report",
            type="primary",
            use_container_width=True,
            key="analyze_sample_btn"
        ):
            run_analysis(SAMPLE_REPORT)


def run_analysis(pdf_text):
    from services.ai_service import generate_analysis

    can_analyze, error_msg = generate_analysis(None, None, check_only=True)
    if not can_analyze:
        st.error(error_msg)
        return

    with st.spinner("🧠 Analyzing your report... This may take 20-30 seconds."):
        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"],
            "Analyzing uploaded blood report...",
            role="user"
        )

        result = generate_analysis(
            {
                "patient_name": "the patient",
                "age": "as mentioned in the report",
                "gender": "as mentioned in the report",
                "report": pdf_text,
            },
            SPECIALIST_PROMPTS["comprehensive_analyst"],
        )

        if result["success"]:
            report_metadata = f"__REPORT_TEXT__\n{pdf_text}\n__END_REPORT_TEXT__"
            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"],
                report_metadata,
                role="system"
            )

            content = result["content"]
            if "model_used" in result:
                content += f"\n\n*Analysis generated using {result['model_used']}*"

            st.session_state.current_report_text = pdf_text
            st.session_state.last_analysis_text = content
            st.session_state.last_patient_name = "Patient"
            st.session_state.last_patient_age = ""
            st.session_state.last_patient_gender = ""

            # Clear uploaded file state
            st.session_state.uploaded_pdf_text = None
            st.session_state.uploaded_file_name = None

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"],
                content,
                role="assistant"
            )
            st.rerun()
        else:
            st.error(
                f"Analysis failed: {result.get('error', 'Unknown error')}")


def show_export_button():
    if st.session_state.get("last_analysis_text"):
        st.markdown("""
            <div style='margin: 1rem 0; padding-top: 1rem;
                border-top: 1px solid rgba(99, 179, 237, 0.1);'>
                <p style='color: #64748B; font-size: 0.75rem; font-weight: 600;
                    letter-spacing: 0.08em; text-transform: uppercase;
                    margin-bottom: 0.5rem;'>Export Report</p>
            </div>
        """, unsafe_allow_html=True)

        show_pdf_export_button(
            patient_name=st.session_state.get("last_patient_name", "Patient"),
            age=st.session_state.get("last_patient_age", ""),
            gender=st.session_state.get("last_patient_gender", ""),
            analysis_text=st.session_state.last_analysis_text,
        )
