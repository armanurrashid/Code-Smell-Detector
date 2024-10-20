import pickle
import re
import numpy as np
import javalang
import streamlit as st

class LargeClassSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/large_class.pkl', 'rb') as model_file:
                self.model = pickle.load(model_file)
        except Exception as e:
            st.error(f"Error loading Large Class model: {e}")
            self.model = None

    def parse_code_to_ast(self, code):
        try:
            return javalang.parse.parse(code)
        except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
            print(f"Error parsing code: {e}")
            return None
        
    def count_loc_from_code(self, code):
        lines = code.splitlines()

        single_line_comment = re.compile(r'^\s*//')
        multi_line_comment_start = re.compile(r'^\s*/\*')
        multi_line_comment_end = re.compile(r'^\s*\*/')

        in_multi_line_comment = False
        loc = 0

        for line in lines:
            line = line.strip()
            if in_multi_line_comment:
                if multi_line_comment_end.match(line):
                    in_multi_line_comment = False
                continue

            if multi_line_comment_start.match(line):
                in_multi_line_comment = True
                continue

            if line and not single_line_comment.match(line):
                loc += 1

        return loc
    
    def count_attributes_from_ast(self, ast_tree):
        if ast_tree is None:
            return 0

        attributes_count = 0

        for _, node in ast_tree:
            if isinstance(node, javalang.tree.FieldDeclaration):
                attributes_count += len(node.declarators)

        return attributes_count

    def predict(self, code):
        if self.model is None:
            return "Model not loaded"
        try:
            loc = self.count_loc_from_code(code)  
            attributes = self.count_attributes_from_ast(self.parse_code_to_ast(code))  

            content_vector = np.array([[loc, attributes]], dtype=float)
            prediction = self.model.predict(content_vector)

            return "Large Class Smell detected" if prediction[0] == 1 else "Large Class Not detected"
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
