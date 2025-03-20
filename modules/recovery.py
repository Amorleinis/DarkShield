import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

def show_procedures():
    st.header("Recovery Procedures")

    tab1, tab2 = st.tabs(["Recovery Plans", "Backup Management"])

    with tab1:
        show_recovery_plans()

    with tab2:
        show_backup_management()

def show_recovery_plans():
    incident_type = st.selectbox(
        "Select Incident Type",
        ["Data Breach", "Ransomware", "System Compromise", "DDoS Attack"]
    )

    show_recovery_checklist(incident_type)
    show_recovery_timeline(incident_type)

def show_backup_management():
    st.subheader("Backup Management")

    # Backup Status Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Last Backup", "2 hours ago", "On Schedule")
    with col2:
        st.metric("Backup Size", "1.2 TB", "+100 MB")
    with col3:
        st.metric("Success Rate", "98%", "+2%")

    # Backup Configuration
    st.subheader("Backup Configuration")
    backup_frequency = st.selectbox(
        "Backup Frequency",
        ["Hourly", "Daily", "Weekly", "Monthly"]
    )

    retention_period = st.slider(
        "Retention Period (days)",
        min_value=7,
        max_value=365,
        value=30
    )

    backup_locations = st.multiselect(
        "Backup Locations",
        ["Local Storage", "Cloud Storage", "Offsite Storage"],
        default=["Local Storage"]
    )

    # Backup History
    st.subheader("Backup History")
    show_backup_history()

    # Restore Options
    st.subheader("Restore Options")
    restore_point = st.date_input(
        "Select Restore Point",
        datetime.now() - timedelta(days=1)
    )

    restore_type = st.radio(
        "Restore Type",
        ["Full System Restore", "Selective Restore", "Configuration Only"]
    )

    if st.button("Initialize Restore"):
        st.warning("Restore process will require system downtime. Please confirm in the next dialog.")
        with st.expander("Restore Confirmation"):
            st.write("Please review restore details:")
            st.write(f"- Restore Point: {restore_point}")
            st.write(f"- Restore Type: {restore_type}")
            st.write(f"- Estimated Duration: 2-4 hours")
            if st.button("Confirm Restore"):
                st.success("Restore process initiated. Monitoring dashboard will show progress.")

def show_backup_history():
    # Sample backup history data
    history = pd.DataFrame({
        'Date': pd.date_range(start=datetime.now()-timedelta(days=7), periods=8, freq='D'),
        'Status': ['Success', 'Success', 'Success', 'Warning', 'Success', 'Success', 'Error', 'Success'],
        'Size': ['1.2 TB', '1.1 TB', '1.1 TB', '1.0 TB', '1.2 TB', '1.1 TB', 'Failed', '1.2 TB'],
        'Duration': ['45 min', '42 min', '44 min', '50 min', '46 min', '43 min', 'N/A', '45 min']
    })

    st.dataframe(
        history.style.apply(lambda x: ['background: red' if v == 'Error' 
                                     else 'background: yellow' if v == 'Warning'
                                     else '' for v in x], subset=['Status'])
    )

def show_recovery_checklist(incident_type):
    st.subheader("Recovery Checklist")
    checklist = get_recovery_checklist(incident_type)
    for item in checklist:
        st.checkbox(item, key=f"check_{item}")

def show_recovery_timeline(incident_type):
    st.subheader("Recovery Timeline")
    timeline = get_recovery_timeline(incident_type)
    df = pd.DataFrame(timeline, columns=["Phase", "Duration", "Description"])
    st.table(df)

def get_recovery_checklist(incident_type):
    checklists = {
        "Data Breach": [
            "✓ Identify compromised data",
            "✓ Notify affected parties",
            "✓ Reset all credentials",
            "✓ Review access logs",
            "✓ Update security policies",
            "→ Restore from verified backup",
            "→ Verify data integrity"
        ],
        "Ransomware": [
            "✓ Isolate infected systems",
            "✓ Assess backup integrity",
            "✓ Restore from clean backups",
            "✓ Update anti-malware solutions",
            "✓ Review security controls",
            "→ Verify system integrity",
            "→ Monitor for reinfection"
        ]
    }
    return checklists.get(incident_type, ["No checklist available for this incident type"])

def get_recovery_timeline(incident_type):
    timelines = {
        "Data Breach": [
            ["Initial Response", "0-24 hours", "Incident identification and containment"],
            ["Investigation", "24-72 hours", "Root cause analysis"],
            ["Remediation", "3-7 days", "System hardening and recovery"],
            ["Review", "1-2 weeks", "Post-incident analysis"]
        ]
    }
    return timelines.get(incident_type, [["N/A", "N/A", "Timeline not available"]])