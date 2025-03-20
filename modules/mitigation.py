import streamlit as st
from utils import nvd_helper
import pandas as pd

def show_strategies():
    st.header("Mitigation Strategies")
    
    threat_type = st.selectbox(
        "Select Threat Type",
        ["SQL Injection", "Cross-Site Scripting", "Buffer Overflow", "Remote Code Execution"]
    )
    
    st.subheader("Recommended Mitigations")
    
    if threat_type == "SQL Injection":
        show_sql_injection_mitigations()
    elif threat_type == "Cross-Site Scripting":
        show_xss_mitigations()
    elif threat_type == "Buffer Overflow":
        show_buffer_overflow_mitigations()
    elif threat_type == "Remote Code Execution":
        show_rce_mitigations()

def show_sql_injection_mitigations():
    mitigations = [
        "Use parameterized queries",
        "Input validation and sanitization",
        "Principle of least privilege",
        "Regular security audits"
    ]
    for m in mitigations:
        st.write(f"• {m}")
    
    with st.expander("Implementation Example"):
        st.code("""
# Example of parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        """)

def show_xss_mitigations():
    mitigations = [
        "Input validation",
        "Output encoding",
        "Content Security Policy (CSP)",
        "HTTP-only cookies"
    ]
    for m in mitigations:
        st.write(f"• {m}")
