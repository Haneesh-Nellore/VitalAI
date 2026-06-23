import streamlit as st
from config.prompts import SPECIALIST_PROMPTS
from utils.pdf_extractor import extract_text_from_pdf
from config.sample_data import SAMPLE_REPORT
from config.app_config import MAX_UPLOAD_SIZE_MB
from components.pdf_export import show_pdf_export_button


def show_analysis_form():
    # Initialize report source in session state for new sessions
    if (
        "current_session" in st.session_state
        and "report_source" not in st.session_state
    ):
        st.session_state.report_source = "Upload PDF"

    report_source = st.radio(
        "Choose report source",
        ["Upload PDF", "Use Sample PDF"],
        index=0 if st.session_state.get("report_source") == "Upload PDF" else 1,
        horizontal=True,
        key="report_source",
    )

    pdf_contents = get_report_contents(report_source)

    if pdf_contents:
        render_patient_form(pdf_contents)


def get_report_contents(report_source):
    if report_source == "Upload PDF":
        uploaded_file = st.file_uploader(
            f"Upload blood report PDF (Max {MAX_UPLOAD_SIZE_MB}MB)",
            type=["pdf"],
            help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB}MB. Only PDF files containing medical reports are supported",
        )
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > MAX_UPLOAD_SIZE_MB:
                st.error(
                    f"File size ({file_size_mb:.1f}MB) exceeds the {MAX_UPLOAD_SIZE_MB}MB limit."
                )
                return None

            if uploaded_file.type != "application/pdf":
                st.error("Please upload a valid PDF file.")
                return None

            pdf_contents = extract_text_from_pdf(uploaded_file)
            if isinstance(pdf_contents, str) and (
                pdf_contents.startswith(
                    ("File size exceeds", "Invalid file type", "Error validating")
                )
                or pdf_contents.startswith("The uploaded file")
                or "error" in pdf_contents.lower()
            ):
                st.error(pdf_contents)
                return None
            with st.expander("View Extracted Report"):
                st.text(pdf_contents)
            return pdf_contents
    else:
        with st.expander("View Sample Report"):
            st.text(SAMPLE_REPORT)
        return SAMPLE_REPORT
    return None


def render_patient_form(pdf_contents):
    with st.form("analysis_form"):
        st.markdown("""
            <p style='
                color: #94A3B8;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
            '>Patient Details</p>
        """, unsafe_allow_html=True)

        patient_name = st.text_input("Patient Name", placeholder="Enter patient name")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.form_submit_button("🔍 Analyze Report", use_container_width=True, type="primary"):
            handle_form_submission(patient_name, age, gender, pdf_contents)


def handle_form_submission(patient_name, age, gender, pdf_contents):
    if not all([patient_name, age, gender]):
        st.error("Please fill in all fields")
        return

    from services.ai_service import generate_analysis

    can_analyze, error_msg = generate_analysis(None, None, check_only=True)
    if not can_analyze:
        st.error(error_msg)
        st.stop()
        return

    with st.spinner("Analyzing your report..."):
        st.session_state.current_report_text = pdf_contents

        # Store patient info for PDF export
        st.session_state.last_patient_name = patient_name
        st.session_state.last_patient_age = age
        st.session_state.last_patient_gender = gender

        st.session_state.auth_service.save_chat_message(
            st.session_state.current_session["id"],
            f"Analyzing report for patient: {patient_name}",
        )

        result = generate_analysis(
            {
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "report": pdf_contents,
            },
            SPECIALIST_PROMPTS["comprehensive_analyst"],
        )

        if result["success"]:
            report_metadata = f"__REPORT_TEXT__\n{pdf_contents}\n__END_REPORT_TEXT__"
            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], report_metadata, role="system"
            )

            content = result["content"]
            if "model_used" in result:
                model_info = f"\n\n*Analysis generated using {result['model_used']}*"
                content += model_info

            # Store analysis for PDF export
            st.session_state.last_analysis_text = content

            st.session_state.auth_service.save_chat_message(
                st.session_state.current_session["id"], content, role="assistant"
            )
            st.rerun()
        else:
            st.error(result["error"])
            st.stop()


def show_export_button():
    """Show PDF export button if analysis is available."""
    if (
        st.session_state.get("last_analysis_text")
        and st.session_state.get("last_patient_name")
    ):
        st.markdown("""
            <div style='
                margin: 1rem 0;
                padding-top: 1rem;
                border-top: 1px solid rgba(99, 179, 237, 0.1);
            '>
                <p style='
                    color: #64748B;
                    font-size: 0.75rem;
                    font-weight: 600;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    margin-bottom: 0.5rem;
                '>Export Report</p>
            </div>
        """, unsafe_allow_html=True)

        show_pdf_export_button(
            patient_name=st.session_state.last_patient_name,
            age=st.session_state.last_patient_age,
            gender=st.session_state.last_patient_gender,
            analysis_text=st.session_state.last_analysis_text,
        )
