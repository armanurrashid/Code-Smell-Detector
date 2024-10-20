import pickle
import re
import numpy as np
import javalang
import streamlit as st

class FunctionalDecompositionSmellDetector:
    def __init__(self):
        try:
            with open('Pkl File/functional_decomposition.pkl', 'rb') as model_file:
                self.model = pickle.load(model_file)
        except Exception as e:
            st.error(f"Error loading Functional Decomposition model: {e}")
            self.model = None

    def parse_code_to_ast(self, code):
        try:
            return javalang.parse.parse(code)
        except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
            print(f"Error parsing code: {e}")
            return None
        
    # def parse_code_to_ast(self, code):
    #     if not re.search(r'class\s+\w+', code):
    #         code = f"public class TemporaryClass {{\n{code}\n}}"
    #         st.write(code)
        
    #     try:
    #         return javalang.parse.parse(code)
    #     except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
    #         st.write(f"Error parsing code: {e}")
    #         return None


    def get_class_tree(self,ast):
        class_tree = {}
        for path, node in ast.filter(javalang.tree.ClassDeclaration):
            class_name = node.name
            parent_name = node.extends.name if node.extends else None
            class_tree[class_name] = parent_name
        return class_tree
    
    def get_methods(self,ast, class_name):
        methods = set()
        for path, node in ast.filter(javalang.tree.MethodDeclaration):
            if isinstance(path[-2], javalang.tree.ClassDeclaration) and path[-2].name == class_name:
                methods.add(node.name)
        return methods
    
    def get_all_parent_methods(self,class_tree, class_name, ast):
        parent_methods = set()
        while class_name in class_tree and class_tree[class_name] is not None:
            class_name = class_tree[class_name]
            parent_methods.update(self.get_methods(ast, class_name))    
        return parent_methods
    
    def calculate_dit(self,class_tree, class_name):
        depth = 0
        while class_name in class_tree and class_tree[class_name] is not None:
            class_name = class_tree[class_name]
            depth += 1
        return depth
    
    def calculate_nmo(self,class_methods, parent_methods):
        return len(class_methods.intersection(parent_methods))  

    def predict(self, code):
        if self.model is None:
            return [("Model not loaded", -1)]
        try:
            ast = self.parse_code_to_ast(code)
            class_tree = self.get_class_tree(ast)
            predictions = []

            for cls in class_tree.keys():
                class_methods = self.get_methods(ast, cls)
                parent_methods = self.get_all_parent_methods(class_tree, cls, ast)
                nmo = self.calculate_nmo(class_methods, parent_methods)
                dit = self.calculate_dit(class_tree, cls) + 1
                content_vector = np.array([[nmo, dit]], dtype=float)
                prediction = self.model.predict(content_vector)[0]
                predictions.append((cls, prediction))
            return predictions
        except Exception as e:
            # st.error(f"Error during predictionFD: {e}")
            return [("Prediction error", -1)]

        
    def get_results(self, java_files):
        combined_content = ""  
        processed_files = set()  

        for file_name, method_name, method_code, content in java_files:
            if file_name not in processed_files:
                processed_files.add(file_name)
                combined_content += content + "\n\n" 

        if combined_content:
            smell_results = self.predict(combined_content)
            
            results = []
            file_names = list(processed_files)  

            class_to_file_map = {}
            for file_name, _, _, content in java_files:
                ast = self.parse_code_to_ast(content)
                class_tree = self.get_class_tree(ast)
                for cls in class_tree.keys():
                    class_to_file_map[cls] = file_name

            for cls, prediction in smell_results:
                file_name = class_to_file_map.get(cls, "Unknown.java")
                result_text = "Smell detected" if prediction == 1 else "FD Not detected"
                results.append((file_name, cls, result_text))
        else:
            results = []  
        
        return results
