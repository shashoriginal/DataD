import streamlit as st
import base64
import pandas as pd
import tempfile
import os
import shutil
import atexit
from sweetviz import analyze as sv_analyze
from dataprep.eda import create_report as dp_create_report

# Function to set a responsive background image
def set_bg_image(image_file):
    with open(image_file, "rb") as file:
        base64_img = base64.b64encode(file.read()).decode()
    bg_image_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(bg_image_style, unsafe_allow_html=True)

# Function to delete temporary files
def clean_up(temp_dir):
    shutil.rmtree(temp_dir)
    st.write(f"Cleaned up temporary directory: {temp_dir}")

# Streamlit UI
def main():
    # Set background image
    set_bg_image("bg.png") 
    
    st.title("DataD 📊: All in One Enhanced Data Analysis App")
    
    # Instructions
    st.markdown("""
        **Instructions**:
        - Upload your CSV file below.
        - We will be adding more EDA Libraries soon!
        - Choose the analysis tool you want to use.
        - The app will generate a comprehensive data analysis report.
        - Use the button to download the report, which you can open in your browser.
        - All files will be deleted once the app is closed.
    """)

    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    analysis_tool = st.selectbox("Choose Analysis Tool", ["DataPrep", "SweetViz"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        temp_dir = tempfile.mkdtemp()
        report_path = os.path.join(temp_dir, f"{analysis_tool.lower()}_report.html")
        
        if analysis_tool == "SweetViz":
            report = sv_analyze(df)
            report.show_html(filepath=report_path, open_browser=False)
        elif analysis_tool == "DataPrep":
            dp_create_report(df).save(report_path)
        
        with open(report_path, "rb") as f:
            btn = st.download_button(
                label=f"Download {analysis_tool} Report",
                data=f,
                file_name=f"{analysis_tool.lower()}_report.html",
                mime="text/html"
            )
        
        atexit.register(clean_up, temp_dir)

footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: white; /* Text color changed to white */
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Made with ❤️ by <a href="https://github.com/shashoriginal" target="_blank" style="color: white;">Shashank</a></p>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
