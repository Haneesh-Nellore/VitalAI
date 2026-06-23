import streamlit as st
import re

def extract_health_metrics(analysis_text):
    """
    Parse AI analysis output and extract key health indicators.
    Returns a dict of metrics with their status.
    """
    metrics = {}
    text_lower = analysis_text.lower()

    # Define health markers to look for
    markers = {
        "Hemoglobin": ["hemoglobin"],
        "Blood Sugar": ["glucose", "blood sugar", "fasting glucose"],
        "Cholesterol": ["cholesterol", "ldl", "hdl"],
        "Triglycerides": ["triglyceride"],
        "White Blood Cells": ["white blood cell", "wbc", "leukocyte"],
        "Platelets": ["platelet"],
        "Kidney Function": ["creatinine", "bun", "kidney"],
        "Liver Function": ["alt", "ast", "bilirubin", "liver"],
        "Thyroid": ["tsh", "thyroid", "t3", "t4"],
    }

    # Classify status based on keywords near the marker
    for metric, keywords in markers.items():
        for keyword in keywords:
            if keyword in text_lower:
                # Look for status indicators near the keyword
                idx = text_lower.find(keyword)
                surrounding = text_lower[max(0, idx-100):idx+200]

                if any(word in surrounding for word in [
                    "critical", "severe", "danger", "abnormal high", "abnormal low",
                    "significantly elevated", "significantly low", "very high", "very low"
                ]):
                    metrics[metric] = "critical"
                elif any(word in surrounding for word in [
                    "borderline", "slightly elevated", "slightly low", "mild",
                    "monitor", "watch", "attention", "upper limit", "lower limit",
                    "risk", "concern", "marginal"
                ]):
                    metrics[metric] = "warning"
                else:
                    metrics[metric] = "normal"
                break

    return metrics

def calculate_health_score(metrics):
    """Calculate overall health score from metrics."""
    if not metrics:
        return 75  # Default score if no metrics found

    score = 100
    for status in metrics.values():
        if status == "critical":
            score -= 20
        elif status == "warning":
            score -= 8

    return max(0, min(100, score))

def get_score_color(score):
    if score >= 80:
        return "#68D391", "Excellent"
    elif score >= 60:
        return "#F6AD55", "Good"
    elif score >= 40:
        return "#FC8181", "Needs Attention"
    else:
        return "#FC4444", "Critical"

def get_status_color(status):
    if status == "normal":
        return "#68D391", "✓ Normal"
    elif status == "warning":
        return "#F6AD55", "⚠ Borderline"
    else:
        return "#FC8181", "✗ Critical"

def show_health_score_dashboard(analysis_text):
    """
    Render the health score dashboard from AI analysis text.
    Call this after generating an analysis.
    """
    if not analysis_text:
        return

    metrics = extract_health_metrics(analysis_text)
    score = calculate_health_score(metrics)
    score_color, score_label = get_score_color(score)

    st.markdown("""
        <style>
            .health-dashboard {
                background: #1E293B;
                border: 1px solid rgba(99, 179, 237, 0.15);
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1.5rem 0;
            }
            .score-circle {
                text-align: center;
                padding: 1rem 0;
            }
            .metric-card {
                background: rgba(15, 23, 42, 0.6);
                border-radius: 10px;
                padding: 0.75rem 1rem;
                margin: 0.4rem 0;
                border: 1px solid rgba(45, 55, 72, 0.8);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='health-dashboard'>", unsafe_allow_html=True)

    # Header
    st.markdown("""
        <p style='
            color: #94A3B8;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 0 0 1rem 0;
        '>🏥 Health Score Dashboard</p>
    """, unsafe_allow_html=True)

    # Score circle
    circumference = 2 * 3.14159 * 54
    dash_offset = circumference * (1 - score / 100)

    st.markdown(f"""
        <div class='score-circle'>
            <svg width="140" height="140" viewBox="0 0 140 140">
                <!-- Background circle -->
                <circle cx="70" cy="70" r="54"
                    fill="none"
                    stroke="rgba(45, 55, 72, 0.8)"
                    stroke-width="10"/>
                <!-- Score arc -->
                <circle cx="70" cy="70" r="54"
                    fill="none"
                    stroke="{score_color}"
                    stroke-width="10"
                    stroke-linecap="round"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{dash_offset}"
                    transform="rotate(-90 70 70)"
                    style="transition: stroke-dashoffset 1s ease;"/>
                <!-- Score text -->
                <text x="70" y="65"
                    text-anchor="middle"
                    font-size="28"
                    font-weight="700"
                    fill="{score_color}"
                    font-family="-apple-system, sans-serif">
                    {score}
                </text>
                <text x="70" y="85"
                    text-anchor="middle"
                    font-size="11"
                    fill="#94A3B8"
                    font-family="-apple-system, sans-serif">
                    out of 100
                </text>
            </svg>
            <p style='
                color: {score_color};
                font-size: 1.1rem;
                font-weight: 600;
                margin: 0.25rem 0 0 0;
                letter-spacing: -0.01em;
            '>{score_label}</p>
            <p style='color: #475569; font-size: 0.8rem; margin: 0.2rem 0 0 0;'>
                Overall Health Score
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Metrics breakdown
    if metrics:
        st.markdown("""
            <p style='
                color: #64748B;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin: 1rem 0 0.5rem 0;
            '>Indicators</p>
        """, unsafe_allow_html=True)

        for metric, status in metrics.items():
            color, label = get_status_color(status)
            st.markdown(f"""
                <div class='metric-card'>
                    <span style='color: #CBD5E0; font-size: 0.88rem;'>{metric}</span>
                    <span style='
                        color: {color};
                        font-size: 0.82rem;
                        font-weight: 600;
                        background: rgba({
                            "104, 211, 145" if status == "normal"
                            else "246, 173, 85" if status == "warning"
                            else "252, 129, 129"
                        }, 0.1);
                        padding: 0.2rem 0.6rem;
                        border-radius: 20px;
                    '>{label}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <p style='color: #475569; font-size: 0.85rem; text-align: center; padding: 1rem 0;'>
                No specific markers detected. See full analysis below.
            </p>
        """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
        <p style='
            color: #334155;
            font-size: 0.72rem;
            text-align: center;
            margin: 1rem 0 0 0;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(45, 55, 72, 0.5);
        '>
            ⚕️ This score is AI-generated and not a substitute for professional medical advice.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
