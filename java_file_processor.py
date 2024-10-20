import zipfile
import streamlit as st
from long_parameter_smell_detector import LongParameterSmellDetector
from large_class_smell_detector import LargeClassSmellDetector
from long_method_smell_detector import LongMethodSmellDetector
from comment_smell_detector import CommentsSmellDetector
from data_class_smell_detector import DataClassSmellDetector
from functional_decomposition_smell import FunctionalDecompositionSmellDetector
import pandas as pd

class JavaFileProcessor:
    def __init__(self):
        self.java_files = []
        self.long_param_detector = LongParameterSmellDetector()
        self.large_class_detector = LargeClassSmellDetector()
        self.long_method_detector = LongMethodSmellDetector()
        self.comment_detector = CommentsSmellDetector()
        self.data_class_detector = DataClassSmellDetector()
        self.functional_decomposition_detector = FunctionalDecompositionSmellDetector()
    
    def process_zip(self, zip_file):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.java'):
                    with zip_ref.open(file_name) as file:
                        content = file.read().decode("utf-8")
                        methods_info = self.long_param_detector.extract_methods(content)
            
                        for method_name, method_code in methods_info:
                            self.java_files.append((file_name, method_name, method_code, content))

    def process_java_files(self, java_files):
        for java_file in java_files:
            content = java_file.read().decode("utf-8")
            methods_info = self.long_param_detector.extract_methods(content)

            for method_name, method_code in methods_info:
                self.java_files.append((java_file.name, method_name, method_code, content))
        # st.write(java_file)
                
    def display_files(self):
        if not self.java_files:
            st.write("No Java files to display.")
            return

        displayed_classes = set()
        # st.write(self.java_files)

        for file_name, method_name, method_code, content in self.java_files:
            if file_name not in displayed_classes:
                with st.expander(f"### {file_name}"):
                    st.text(f"Code:\n{content}")
                displayed_classes.add(file_name)
                
    def display_results(self):
        tables_to_display = []

        if self.java_files:
            results_large_class = self.large_class_detector.get_results(self.java_files)
            filtered_results_large_class = [item for item in results_large_class if item[1] != "Large Class Not detected"]
            if filtered_results_large_class:
                df_largeClass = pd.DataFrame(filtered_results_large_class, columns=["File Name", "Large Class Smell"])
                tables_to_display.append(("### Large Class Smell Results", df_largeClass))

        if self.java_files:
            results_comment = self.comment_detector.get_results(self.java_files)
            filtered_results_comments = [item for item in results_comment if item[1] != "No Comment smell detected"]
            if filtered_results_comments:
                df_comment = pd.DataFrame(filtered_results_comments, columns=["File Name", "Comment Smell"])
                tables_to_display.append(("### Comment Smell Results", df_comment))

        if self.java_files:
            results_long_param = self.long_param_detector.get_results(self.java_files)
            filtered_results_long_param = [item for item in results_long_param if item[2] != "No LP smell detected"]
            if filtered_results_long_param:
                df_longparam = pd.DataFrame(filtered_results_long_param, columns=["File Name", "Method Name", "Long Parameter Smell"])
                tables_to_display.append(("### Long Parameter Smell Results", df_longparam))

        if self.java_files:
            results_long_method = self.long_method_detector.get_results(self.java_files)
            filtered_results_long_method = [item for item in results_long_method if item[2] != "Long Method Not detected"]
            if filtered_results_long_method:
                df_longMethod = pd.DataFrame(filtered_results_long_method, columns=["File Name", "Method Name", "Long Method Smell"])
                tables_to_display.append(("### Long Method Smell Results", df_longMethod))

        if self.java_files:
            results_data_class = self.data_class_detector.get_results(self.java_files)
            filtered_results_data_class = [item for item in results_data_class if item[1] != "Data Class Not detected"]
            if filtered_results_data_class:
                df_dataClass = pd.DataFrame(filtered_results_data_class, columns=["File Name", "Data Class Smell"])
                tables_to_display.append(("### Data Class Smell Results", df_dataClass))

        if self.java_files:
            results_functional_decomposition = self.functional_decomposition_detector.get_results(self.java_files)
            filtered_results_functional_decomposition = [item for item in results_functional_decomposition if item[2] != "FD Not detected"]
            if filtered_results_functional_decomposition:
                df_functional_decomposition = pd.DataFrame(filtered_results_functional_decomposition, columns=["File Name", "Class", "Functional Decomposition Smell"])
                tables_to_display.append(("### FD Smell Results", df_functional_decomposition))

        if tables_to_display:
            for i in range(0, len(tables_to_display), 2):
                cols = st.columns(2) 
                for j, (title, df) in enumerate(tables_to_display[i:i + 2]):
                    with cols[j]:
                        st.markdown(title)
                        st.dataframe(df, use_container_width=True)
        else:
            st.write("No smell results to display.")

        # col1, col2 = st.columns(2)
        # with col1:
        #     if self.java_files:
        #         results = self.large_class_detector.get_results(self.java_files)
        #         filtered_results = [item for item in results if item[1]!= "Large Class Not detected"]
        #         if filtered_results:
        #             st.markdown("### Large Class Smell Results")
        #             df_largeClass = pd.DataFrame(filtered_results, columns=["File Name", "Large Class Smell"])
        #             st.dataframe(df_largeClass, use_container_width=True)
        #     else:
        #         st.write("No Large Class Smell results to display.")
            
        # with col2:
        #     if self.java_files:
        #         results = self.comment_detector.get_results(self.java_files)
        #         filtered_results = [item for item in results if item[1]!= "No Comment smell detected"]
        #         if filtered_results:
        #             st.markdown("### Comment Smell Results")
        #             df_comment = pd.DataFrame(filtered_results, columns=["File Name", "Comment Smell"])
        #             st.dataframe(df_comment, use_container_width=True)
        #     else:
        #         st.write("No Comments Smell results to display.")

        # col1, col2 = st.columns(2)
        # with col1:
        #     if self.java_files:
        #         results = self.long_param_detector.get_results(self.java_files)
        #         filtered_results = [item for item in results if item[2] != "No LP smell detected"]
        #         if filtered_results:
        #             st.markdown("### Long Parameter Smell Results")
        #             df_longparam = pd.DataFrame(filtered_results, columns=["File Name", "Method Name", "Long Parameter Smell"])
        #             st.dataframe(df_longparam, use_container_width=True)
        #     else:
        #         st.write("No Long Parameter Smell results to display.")

        # with col2:
        #     if self.java_files:
        #         results = self.long_method_detector.get_results(self.java_files)
        #         filtered_results = [item for item in results if item[2] != "Long Method Not detected"]

        #         if filtered_results:
        #             st.markdown("### Long Method Smell Results")
        #             df_longMethod = pd.DataFrame(filtered_results, columns=["File Name", "Method Name", "Long Method Smell"])
        #             st.dataframe(df_longMethod, use_container_width=True)
        #     else:
        #         st.write("No Long Method Smell results to display.")
                
        # col1, col2 = st.columns(2)
        # with col1:
        #     if self.java_files:
        #         results = self.data_class_detector.get_results(self.java_files)
                
        #         filtered_results = [item for item in results if item[1]!= "Data Class Not detected"]
        #         if filtered_results:
        #             st.markdown("### Data Class Smell Results")
        #             df_dataClass = pd.DataFrame(filtered_results, columns=["File Name", "Data Class Smell"])
        #             st.dataframe(df_dataClass, use_container_width=True)
        #     else:
        #         st.write("No Data Class Smell results to display.")

        # with col2:
        #     if self.java_files:
        #         results = self.functional_decomposition_detector.get_results(self.java_files)
        #         filtered_results = [item for item in results if item[2] != "FD Not detected"]
        #         if filtered_results:
        #             st.markdown("### FD Smell Results")
        #             df_functional_decomposition_detector = pd.DataFrame(filtered_results, columns=["File Name", "Class", "Functional Decomposition Smell"])
        #             st.dataframe(df_functional_decomposition_detector, use_container_width=True)
        #     else:
        #         st.write("No Functional Decomposition Smell results to display.")
