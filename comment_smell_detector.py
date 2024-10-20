import pickle
import re
import numpy as np
import streamlit as st

class CommentsSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/comments.pkl', 'rb') as model_file:
                self.model = pickle.load(model_file)
        except Exception as e:
            st.error(f"Error loading Long Parameter model: {e}")
            self.model = None

    def count_comments_percentage(self,code):
        lines = code.splitlines()

        single_line_comment = re.compile(r'^\s*//')
        multi_line_comment_start = re.compile(r'^\s*/\*')
        multi_line_comment_end = re.compile(r'.*\*/')

        in_multi_line_comment = False
        loc = 0
        comment_lines = 0

        for line in lines:
            line = line.strip()

            # Check if we are inside a multi-line comment
            if in_multi_line_comment:
                loc += 1
                comment_lines += 1
                if multi_line_comment_end.search(line):
                    in_multi_line_comment = False
                continue

            # Check for multi-line comment start
            if multi_line_comment_start.match(line):
                in_multi_line_comment = True
                loc += 1
                comment_lines += 1
                if multi_line_comment_end.search(line):
                    in_multi_line_comment = False
                continue

            # Check for single-line comments
            if single_line_comment.match(line):
                comment_lines += 1

            # Exclude blank lines
            if line:
                loc += 1
        comment_percentage = round((comment_lines / loc) * 100) if loc > 0 else 0

        return comment_percentage

    def predict(self, code):
        if self.model is None:
            return "Model not loaded"
        param_count = self.count_comments_percentage(code)
        param_vector = np.array([[param_count]])
        try:
            prediction = self.model.predict(param_vector)
            return "Smell detected" if prediction[0] == 1 else "No Comment smell detected"
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            return "Prediction error"
    
    def get_results(self, java_files):
        results = []
        processed_files = set()

        for file_name, method_name, method_code, content in java_files:
            if file_name not in processed_files:
                processed_files.add(file_name)
                smell_result = self.predict(content)
                results.append((file_name, smell_result))
        return results
