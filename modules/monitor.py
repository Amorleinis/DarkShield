import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_metric_chart():
    # Create sample monitoring data
    dates = pd.date_range(start=datetime.now() - timedelta(hours=24), 
                         end=datetime.now(), freq='H')
    cpu_usage = np.random.uniform(20, 80, len(dates))
    memory_usage = np.random.uniform(30, 90, len(dates))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=cpu_usage, name="CPU Usage"))
    fig.add_trace(go.Scatter(x=dates, y=memory_usage, name="Memory Usage"))
    fig.update_layout(title="System Resource Usage", xaxis_title="Time", yaxis_title="Usage %")
    return fig

def show_dashboard():
    st.header("System Monitoring Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Threats", "2", "-1")
    with col2:
        st.metric("System Health", "98%", "+2%")
    with col3:
        st.metric("Security Score", "85/100", "+5")
    
    st.plotly_chart(create_metric_chart(), use_container_width=True)
    
    with st.expander("Active Monitoring Metrics"):
        st.write("• Network Traffic Analysis")
        st.write("• System Resource Usage")
        st.write("• Security Event Logs")
        st.write("• User Activity Monitoring")
