"""
Main Dashboard Application
University Analytics Dashboard - Streamlit Version
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="University Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Navigation")
    
    page = st.sidebar.radio(
        "Select Page:",
        ["🏠 Home", "📈 Overview", "👥 Student Analytics", "📚 Academic Programs", "💰 Finance", "⚙️ Settings"]
    )
    
    # Main content
    if page == "🏠 Home":
        st.title("🎓 University Analytics Dashboard")
        st.write("""
            Welcome to the University Analytics Dashboard!
            
            This dashboard provides comprehensive insights into university operations,
            student demographics, academic performance, and financial metrics.
        """)
        
    elif page == "📈 Overview":
        st.title("📈 Overview")
        st.info("Overview page - Coming soon!")
        
    elif page == "👥 Student Analytics":
        st.title("👥 Student Analytics")
        st.info("Student Analytics page - Coming soon!")
        
    elif page == "📚 Academic Programs":
        st.title("📚 Academic Programs")
        st.info("Academic Programs page - Coming soon!")
        
    elif page == "💰 Finance":
        st.title("💰 Finance")
        st.info("Finance page - Coming soon!")
        
    elif page == "⚙️ Settings":
        st.title("⚙️ Settings")
        st.info("Settings page - Coming soon!")

if __name__ == "__main__":
    main()
