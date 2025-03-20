import streamlit as st
from utils import nvd_helper, exploit_db
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def show_detection():
    st.header("Threat Detection System")

    tab1, tab2, tab3 = st.tabs(["CVE Monitor", "Exploit Database", "Vulnerability Analysis"])

    with tab1:
        st.subheader("Recent CVE Entries")

        # Add filters
        col1, col2 = st.columns(2)
        with col1:
            days_back = st.slider("Days to look back", 1, 30, 7)
        with col2:
            severity_filter = st.selectbox(
                "Filter by Severity",
                ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
                index=0
            )

        # Get CVE data
        cve_data = nvd_helper.get_recent_cves(
            days_back=days_back,
            severity_filter=None if severity_filter == "All" else severity_filter
        )

        if cve_data:
            df = pd.DataFrame(
                cve_data,
                columns=["CVE ID", "Description", "CVSS Score", "Published Date", 
                        "Severity", "Vector String", "Attack Vector"]
            )

            # Add severity coloring
            def color_severity(val):
                if val == 'CRITICAL':
                    return 'background-color: #ff0000; color: white'
                elif val == 'HIGH':
                    return 'background-color: #ffcccc'
                elif val == 'MEDIUM':
                    return 'background-color: #ffffcc'
                return 'background-color: #ccffcc'

            # Display the dataframe with styling
            st.dataframe(
                df.style.applymap(color_severity, subset=['Severity'])
            )

            # Allow detailed view of specific CVE
            selected_cve = st.selectbox("Select CVE for detailed information", df["CVE ID"])
            if selected_cve:
                details = nvd_helper.get_cve_details(selected_cve)
                if details:
                    with st.expander("CVE Details"):
                        st.write("### Basic Information")
                        st.write(f"**Published:** {details['published']}")
                        st.write(f"**Last Modified:** {details['lastModified']}")
                        st.write("**Description:**")
                        st.write(details['description'])

                        st.write("### CVSS Metrics")
                        for version, metrics in details['metrics'].items():
                            st.write(f"**CVSS {version}**")
                            cols = st.columns(3)
                            with cols[0]:
                                st.metric("Base Score", metrics.get('baseScore', 'N/A'))
                            with cols[1]:
                                st.metric("Severity", metrics.get('severity', 'N/A'))
                            with cols[2]:
                                st.metric("Attack Vector", metrics.get('attackVector', 'N/A'))

                            if version == 'v31':  # Show detailed metrics for v3.1
                                st.write("**Detailed Metrics:**")
                                detailed_cols = st.columns(3)
                                with detailed_cols[0]:
                                    st.write("Attack Complexity:", metrics.get('attackComplexity', 'N/A'))
                                    st.write("Privileges Required:", metrics.get('privilegesRequired', 'N/A'))
                                with detailed_cols[1]:
                                    st.write("User Interaction:", metrics.get('userInteraction', 'N/A'))
                                    st.write("Scope:", metrics.get('scope', 'N/A'))
                                with detailed_cols[2]:
                                    st.write("Confidentiality:", metrics.get('confidentialityImpact', 'N/A'))
                                    st.write("Integrity:", metrics.get('integrityImpact', 'N/A'))

                        st.write("### References")
                        for ref in details['references']:
                            st.write(f"- {ref}")
        else:
            st.error("Unable to fetch CVE data. Please check your connection.")

    with tab2:
        st.subheader("Latest Exploit Database Entries")
        exploit_data = exploit_db.get_recent_exploits()
        if exploit_data:
            st.dataframe(
                pd.DataFrame(exploit_data,
                           columns=["ID", "Title", "Type", "Platform", "Date"])
            )
        else:
            st.error("Unable to fetch Exploit-DB data. Please check your connection.")

    with tab3:
        st.subheader("Vulnerability Trends Analysis")
        analysis = nvd_helper.analyze_vulnerability_trends(days_back)
        if analysis:
            # Metrics Overview
            st.write("### Security Metrics Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total CVEs", analysis['total_cves'])
            with col2:
                st.metric("Critical Severity", analysis['critical_severity'])
            with col3:
                st.metric("High Severity", analysis['high_severity'])
            with col4:
                st.metric("Medium Severity", analysis['medium_severity'])

            # Severity Distribution
            st.write("### Severity Distribution")
            severity_data = {
                'Severity': ['Critical', 'High', 'Medium', 'Low'],
                'Count': [
                    analysis['critical_severity'],
                    analysis['high_severity'],
                    analysis['medium_severity'],
                    analysis['low_severity']
                ]
            }
            fig = px.pie(severity_data, values='Count', names='Severity',
                        color_discrete_sequence=['red', 'orange', 'yellow', 'green'])
            st.plotly_chart(fig)

            # Attack Vector Analysis
            st.write("### Attack Vector Distribution")
            attack_vectors = pd.DataFrame(
                list(analysis['attack_vectors'].items()),
                columns=['Attack Vector', 'Count']
            )
            fig = px.bar(attack_vectors, x='Attack Vector', y='Count')
            st.plotly_chart(fig)

            # Daily Trend
            st.write("### Daily Vulnerability Trends")
            daily_data = pd.DataFrame(
                list(analysis['daily_counts'].items()),
                columns=['Date', 'Count']
            )
            fig = px.line(daily_data, x='Date', y='Count')
            st.plotly_chart(fig)

            if analysis['highest_score']:
                st.write("### Highest Risk Vulnerability")
                st.write(f"**CVE:** {analysis['highest_score']['id']}")
                st.write(f"**Score:** {analysis['highest_score']['score']}")
                st.write(f"**Description:** {analysis['highest_score']['description']}")