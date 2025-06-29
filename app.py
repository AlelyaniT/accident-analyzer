import streamlit as st
from PIL import Image
import processing
import os

# Configure the app
st.set_page_config(page_title="Accident Analyzer", layout="wide")
st.title("🚗 Saudi Accident Scene Analyzer (Prototype)")
st.markdown("""
    *AI-powered accident reconstruction for Saudi traffic law compliance*  
    *Note: This is a simulation for demo purposes*
""")

# Sidebar with settings
with st.sidebar:
    st.header("Settings")
    language = st.radio("Report Language", ["English", "Arabic/English"])
    law_version = st.selectbox("Traffic Law Version", ["Saudi Arabia", "UAE", "Kuwait"])

# Upload section
uploaded_files = st.file_uploader(
    "Upload accident scene image(s)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        original_img = Image.open(uploaded_files[0])
        st.image(original_img, use_column_width=True)
    
    if st.button("Analyze Accident", type="primary"):
        with st.spinner("🔍 Detecting vehicles, damage, and road signs..."):
            # Process image (simulated or real YOLOv8)
            processed_img = processing.detect_objects(original_img)
            reconstructed_img = processing.generate_reconstruction(original_img)
            
            # Generate report
            report_data = processing.analyze_scene(original_img, law_version)
            
            with col2:
                st.subheader("AI Analysis")
                st.image(processed_img, caption="Damage & Object Detection", use_column_width=True)
                st.image(reconstructed_img, caption="3D Scene Reconstruction", use_column_width=True)
            
            # Show results
            st.success("Analysis Complete!")
            with st.expander("📝 Legal Assessment"):
                st.markdown(f"""
                **Responsibility:** {report_data['responsibility']}  
                **Legal Basis:** {report_data['law_reference']}  
                **Confidence:** {report_data['confidence']}%  
                """)
            
            # PDF report
            pdf_path = processing.generate_report(report_data, "ar_en" if language == "Arabic/English" else "en")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📄 Download Full Report", 
                    f, 
                    file_name="accident_report.pdf",
                    mime="application/pdf"
                )

# Add sample images for quick testing
st.sidebar.markdown("---")
st.sidebar.subheader("Try Sample Accidents")
sample_files = ["sample1.jpg", "sample2.jpg"]  # Add your sample images
for sample in sample_files:
    if st.sidebar.button(f"Load {sample}"):
        st.session_state.uploaded_file = open(sample, "rb")
        st.rerun()