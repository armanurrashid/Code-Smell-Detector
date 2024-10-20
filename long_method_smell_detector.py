import pickle
import re
import numpy as np
import javalang
import streamlit as st

class LongMethodSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/long_method.pkl', 'rb') as model_file:
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

    def wrap_method_in_class(self, method_code):
        class_code = f"""
        public class Temp {{
            {method_code}
        }}
        """
        return class_code

    def calculate_cyclomatic_complexity(self, method_code):
        try:
            wrapped_code = self.wrap_method_in_class(method_code)
            tree = javalang.parse.parse(wrapped_code)
            # tree = javalang.parse.parse(method_code)
            complexity = 1

            for path, node in tree:
                if isinstance(node, (javalang.tree.IfStatement,
                                    javalang.tree.ForStatement,
                                    javalang.tree.WhileStatement,
                                    javalang.tree.DoStatement,
                                    javalang.tree.SwitchStatement,
                                    javalang.tree.CatchClause)):
                    complexity += 1

            return complexity

        except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
            print(f"Error parsing method: {e}")
            return None


    def longMethodPredict(self, code):
        # st.write(code)
        if self.model is None:
            return "Model not loaded"
        try:
            complexity = self.calculate_cyclomatic_complexity(code)  
            
            content_vector = np.array(complexity).reshape(1, -1)
            prediction = self.model.predict(content_vector)

            return "Long Method Smell detected" if prediction[0] == 1 else "Long Method Not detected"
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            return "Prediction error"

    # def get_results(self, java_files):
    #     results = []
    #     processed_files = set()

    #     for file_name, method_name, method_code, content in java_files:
    #         if file_name not in processed_files:
    #             processed_files.add(file_name)
    #             smell_result = self.longMethodPredict(method_code)
    #             results.append((file_name,method_name,  smell_result))
    #     return results

    def get_results(self, java_files):
        results = []
        for file_name, method_name, method_code, content in java_files:
            smell_result = self.longMethodPredict(content)
            results.append((file_name, method_name, smell_result))
        return results

