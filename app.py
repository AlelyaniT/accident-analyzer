import streamlit as st
from PIL import Image
from processing import AccidentAnalyzer
import os

# Configure the app
st.set_page_config(page_title="Accident Analyzer", layout="wide")
st.title("🚗 Saudi Accident Scene Analyzer")
st.markdown("""
    *AI-powered accident reconstruction for Saudi traffic law compliance*  
    *Note: This is a simulation for demo purposes*
""")

# Initialize analyzer
analyzer = AccidentAnalyzer()

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
        st.image(original_img, use_container_width=True)  # Updated parameter
    
    if st.button("Analyze Accident", type="primary"):
        with st.spinner("🔍 Analyzing scene..."):
            # Process image
            processed_img = analyzer.detect_objects(original_img)
            reconstructed_img = analyzer.generate_reconstruction(original_img)
            
            # Generate report
            report_data = analyzer.analyze_scene(original_img, law_version)
            
            with col2:
                if processed_img:
                    st.subheader("AI Analysis")
                    st.image(processed_img, caption="Damage & Object Detection", use_container_width=True)
                    st.image(reconstructed_img, caption="3D Scene Reconstruction", use_container_width=True)
                else:
                    st.error("Image processing failed - check logs")
            
            # Show results
            if processed_img:
                st.success("Analysis Complete!")
                with st.expander("📝 Legal Assessment"):
                    st.markdown(f"""
                    **Responsibility:** {report_data['responsibility']}  
                    **Legal Basis:** {report_data['law_reference']}  
                    **Confidence:** {report_data['confidence']}%  
                    """)

                # PDF report
                pdf_path = analyzer.generate_report(
                    report_data, 
                    "ar_en" if language == "Arabic/English" else "en"
                )
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📄 Download Full Report", 
                            f, 
                            file_name="accident_report.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.warning("PDF report generation failed")

# Sample images for testing
st.sidebar.markdown("---")
st.sidebar.subheader("Try Sample Accidents")
if st.sidebar.button("Load Sample Accident 1"):
    try:
        original_img = Image.open("sample_images/sample1.jpg")
        st.session_state.uploaded_file = original_img
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"Failed to load sample: {e}")
