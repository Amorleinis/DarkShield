import streamlit as st
from utils import simulation
import plotly.graph_objects as go

def show_scenarios():
    st.header("Isolation Scenario Simulations")
    
    scenario = st.selectbox(
        "Select Isolation Scenario",
        ["Network Segmentation", "Container Isolation", "Process Isolation"]
    )
    
    if scenario == "Network Segmentation":
        st.subheader("Network Segmentation Simulation")
        segments = st.multiselect(
            "Select network segments to isolate:",
            ["Production", "Development", "Database", "DMZ"]
        )
        
        if st.button("Run Simulation"):
            results = simulation.run_network_isolation(segments)
            st.plotly_chart(
                simulation.create_network_graph(results),
                use_container_width=True
            )
    
    elif scenario == "Container Isolation":
        st.subheader("Container Isolation Simulation")
        container_count = st.slider("Number of Containers", 1, 10, 3)
        
        if st.button("Simulate Container Isolation"):
            results = simulation.run_container_isolation(container_count)
            st.json(results)
    
    elif scenario == "Process Isolation":
        st.subheader("Process Isolation Simulation")
        process_name = st.text_input("Enter Process Name")
        
        if st.button("Simulate Process Isolation"):
            results = simulation.run_process_isolation(process_name)
            st.code(results)
