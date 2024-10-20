import pickle
import re
import numpy as np
import javalang
import streamlit as st

class LongParameterSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/long_parameter.pkl', 'rb') as model_file:
                self.model = pickle.load(model_file)
        except Exception as e:
            st.error(f"Error loading Long Parameter model: {e}")
            self.model = None

    def extract_methods(self,java_code):
        method_pattern = re.compile(
            r'(?P<signature>(?:public|protected|private|static|final|synchronized|native|abstract|transient|volatile)?\s*'
            r'(?:[\w<>\[\]]+\s+)+\w+\s*\([^)]*\)\s*(?:throws\s+\w+(?:,\s*\w+)*)?)\s*{',
            re.DOTALL
        )

        
        methods = []
        
        for match in method_pattern.finditer(java_code):
            signature = match.group('signature').strip()
            start_index = match.start()
            open_braces = 1
            end_index = None
            
            for i in range(start_index + len(match.group(0)), len(java_code)):
                if java_code[i] == '{':
                    open_braces += 1
                elif java_code[i] == '}':
                    open_braces -= 1
                    if open_braces == 0:
                        end_index = i + 1
                        break
            
            if end_index is None:
                continue
            
            full_code = java_code[start_index:end_index].strip()
            method_name = signature.split('(')[0].split()[-1]
            if method_name.lower() in ('if', 'else', 'else if'):
                continue
            methods.append((method_name, full_code))
        
        return methods
        
    def parse_code_to_ast_and_count_params(self, code):
        try:
            ast_tree = javalang.parse.parse_member_signature(code)
            if isinstance(ast_tree, javalang.tree.MethodDeclaration):
                return len(ast_tree.parameters)
            else:
                return 0
        except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError):
            return 0

    def predict(self, code):
        if self.model is None:
            return "Model not loaded"
        param_count = self.parse_code_to_ast_and_count_params(code)
        param_vector = np.array([[param_count]])
        try:
            prediction = self.model.predict(param_vector)
            return "Smell detected" if prediction[0] == 1 else "No LP smell detected"
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            return "Prediction error"
    
    def get_results(self, java_files):
        results = []
        for file_name, method_name, method_code, content in java_files:
            smell_result = self.predict(method_code)
            results.append((file_name, method_name, smell_result))
        return results
