import streamlit as st
from css_style import CSSStyle
from sidebar import Sidebar
from java_file_processor import JavaFileProcessor

st.set_page_config(page_title="Code Smell Detector", page_icon="💩",layout="wide")

def main():
    CSSStyle.inject_css()
    st.markdown("<h1 style='text-align : center; padding-bottom : 3rem;'>💩 Code Smell Detector</h1>",unsafe_allow_html=True)
    selected = Sidebar.display_sidebar()
    file_processor = JavaFileProcessor()

    uploaded_files = st.file_uploader(
        "Choose a ZIP file or multiple Java files",
        type=["zip", "java"],
        accept_multiple_files=True,
        key="file_uploader"
    )

    if uploaded_files:
        zip_files = []
        java_files = []

        for file in uploaded_files:
            if file.name.endswith('.zip'):
                zip_files.append(file)
            elif file.name.endswith('.java'):
                java_files.append(file)
        
        if zip_files:
            for zip_file in zip_files:
                file_processor.process_zip(zip_file)
    
        if java_files:
            file_processor.process_java_files(java_files)

        file_processor.display_files()
        file_processor.display_results()

if __name__ == "__main__":
    main()

#.\env\Scripts\activate   streamlit run main.py