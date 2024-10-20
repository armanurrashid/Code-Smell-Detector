import pickle
import re
import numpy as np
import javalang
import streamlit as st

class DataClassSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/data_class.pkl', 'rb') as model_file:
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
        
    def is_getter_or_setter(self,method_node):
        method_name = method_node.name
        return (method_name.startswith('get') or
                method_name.startswith('set') or
                method_name.startswith('is')) and len(method_node.parameters) <= 1
    
    def is_data_class(self,class_node):
        method_count = 0
        getter_setter_count = 0

        for member in class_node.body:
            if isinstance(member, javalang.tree.MethodDeclaration):
                method_count += 1
                if self.is_getter_or_setter(member):
                    getter_setter_count += 1

        return method_count, getter_setter_count
    
    def find_data_classes(self,code):
        tree = self.parse_code_to_ast(code)
        if tree is None:
            return 0, 0

        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            method_count, getter_setter_count = self.is_data_class(node)

        return method_count, getter_setter_count

    def predict(self, code):
        if self.model is None:
            return "Model not loaded"
        try:
            method_count, getter_setter_count = self.find_data_classes(code)
            content_vector = np.array([[method_count, getter_setter_count]], dtype=float)
            prediction = self.model.predict(content_vector)

            return "Data Class Smell detected" if prediction[0] == 1 else "Data Class Not detected"
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
