import streamlit as st

class Sidebar:
    @staticmethod
    def display_sidebar():
        selected = st.sidebar.selectbox(
            "Code Smells",
            options=["Please select", "Large Class", "Long Parameter List", "Long Method", "Comment", "Data Class", "Functional Decomposition"]
        )
        
        if selected == "Large Class":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("A class contains many fields, methods or lines of code.")
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            Classes usually start small. But over time, they get bloated as the program grows. As is the case with long methods as well, programmers usually find it mentally less taxing to place a new feature in an existing class than to create a new class for the feature.
            </div>
            """, unsafe_allow_html=True)
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Extract Class
            - Extract Subclass
            - Extract Interface
            """)
            st.sidebar.markdown("### Reference")
            st.sidebar.write("https://refactoring.guru/smells/large-class")
        elif selected == "Long Parameter List":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("A method contains more than three parameters")
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            A long list of parameters might happen after several types of algorithms are merged in a single method. It’s hard to understand such lists, which become contradictory and hard to use as they grow longer. Instead of a long list of parameters, a method can use the data of its own object.
            </div>
            """, unsafe_allow_html=True)
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Preserve Whole Object
            - Introduce Parameter Object
            - Replace Parameter with Method Call
            """)
            st.sidebar.markdown("### Reference")
            st.sidebar.write("https://refactoring.guru/smells/long-parameter-list")
        elif selected == "Long Method":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("A method contains too many lines of code.")
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            Like the Hotel California, something is always being added to a method but nothing is ever taken out. Since it’s easier to write code than to read it, this “smell” remains unnoticed until the method turns into an ugly, oversized beast.
            </div>
            """, unsafe_allow_html=True)
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Extract Method
            - Replace Temp with Query
            - Introduce Parameter Object
            - Replace Method with Method Object
            """)
            st.sidebar.markdown("### Reference")
            st.sidebar.write("https://refactoring.guru/smells/long-method")
        elif selected == "Data Class":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("A class contains only field not functionality.")
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            It’s a normal thing when a newly created class contains only a few public fields (and maybe even a handful of getters/setters). But the true power of objects is that they can contain behavior types or operations on their data.
            </div>
            """, unsafe_allow_html=True)
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Move Method
            - Extract Method
            - Encapsulate Field
            """)
            st.sidebar.markdown("### Reference")
            st.sidebar.write("https://refactoring.guru/smells/data-class")
        elif selected == "Functional Decomposition":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("A class or module is split into multiple small functions, each doing a specific task, which can lead to an over-complication of simple logic.")
            
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            Functional decomposition can lead to code that is difficult to follow and maintain, as excessive splitting of logic can make the overall flow less clear. While breaking down tasks can be beneficial, doing so excessively may result in unnecessary complexity and fragmented functionality.
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Combine Related Functions
            - Use Object-Oriented Principles
            - Simplify the Logic
            """)
        elif selected == "Comment":
            st.sidebar.markdown("### Signs and Symptoms") 
            st.sidebar.write("Comments are used excessively or to explain code that is already clear, leading to cluttered and confusing code.")
            
            st.sidebar.markdown("### Reasons for the Problem")
            st.sidebar.markdown("""
            <div style="text-align: justify;">
            Commenting is a useful tool for clarification, but over-relying on comments can indicate that the code itself is not clear or well-structured. If the logic is difficult to understand without comments, it might need refactoring or simplification.
            </div>
            """, unsafe_allow_html=True)
            
            st.sidebar.markdown("### Treatment")
            st.sidebar.markdown("""
            - Refactor Code for Clarity
            - Use Meaningful Variable and Function Names
            - Remove Unnecessary Comments
            """)
            
            # st.sidebar.markdown("### Reference")
            # st.sidebar.write("https://refactoring.guru/smells/comment")

            
            # st.sidebar.markdown("### Reference")
            # st.sidebar.write("https://refactoring.guru/smells/functional-decomposition")


        
        
        return selected
