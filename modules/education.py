import streamlit as st

def show_content():
    st.header("Security Education Center")
    
    tab1, tab2, tab3 = st.tabs(["Security Lifecycle", "Best Practices", "Case Studies"])
    
    with tab1:
        show_security_lifecycle()
    
    with tab2:
        show_best_practices()
    
    with tab3:
        show_case_studies()

def show_security_lifecycle():
    st.subheader("Security Lifecycle Phases")
    
    phases = {
        "Monitoring": "Continuous observation of system and network activities",
        "Detection": "Identifying potential security threats and vulnerabilities",
        "Isolation": "Containing and segregating affected systems",
        "Mitigation": "Implementing corrective measures",
        "Recovery": "Restoring systems to normal operation"
    }
    
    for phase, description in phases.items():
        with st.expander(phase):
            st.write(description)

def show_best_practices():
    st.subheader("Security Best Practices")
    
    practices = [
        "Regular Security Audits",
        "Principle of Least Privilege",
        "Defense in Depth",
        "Regular Backups",
        "Incident Response Planning"
    ]
    
    for practice in practices:
        with st.expander(practice):
            st.write(f"Details about {practice}")

def show_case_studies():
    st.subheader("Security Case Studies")
    
    case_studies = {
        "Major Data Breach Analysis": """
        A detailed analysis of a significant data breach incident, including:
        - Initial compromise
        - Detection timeline
        - Response measures
        - Lessons learned
        """,
        "Ransomware Recovery": """
        Study of a successful ransomware recovery:
        - Initial impact
        - Containment strategy
        - Recovery process
        - Preventive measures
        """
    }
    
    for title, content in case_studies.items():
        with st.expander(title):
            st.write(content)
