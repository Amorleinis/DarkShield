import streamlit as st
from modules import monitor, threat_detection, isolation, mitigation, recovery, education, pentest

st.set_page_config(
    page_title="Security Lifecycle Demo",
    page_icon="🛡️",
    layout="wide"
)

def main():
    st.title("Security Lifecycle Demonstration Tool")

    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Threat Detection", "Penetration Testing", "Isolation Scenarios", 
         "Mitigation Strategies", "Recovery Procedures", "Education Center"]
    )

    if menu == "Dashboard":
        monitor.show_dashboard()
    elif menu == "Threat Detection":
        threat_detection.show_detection()
    elif menu == "Penetration Testing":
        pentest.show_pentest()
    elif menu == "Isolation Scenarios":
        isolation.show_scenarios()
    elif menu == "Mitigation Strategies":
        mitigation.show_strategies()
    elif menu == "Recovery Procedures":
        recovery.show_procedures()
    elif menu == "Education Center":
        education.show_content()

if __name__ == "__main__":
    main()