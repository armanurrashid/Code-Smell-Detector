# css_manager.py

import streamlit as st


class CSSStyle:
    @staticmethod
    def inject_css():
        st.markdown("""
            <style>
            .st-emotion-cache-sesqrs a{
                color: rgb(0 0 0);
            }
            .st-emotion-cache-1jicfl2 {
                padding: 3rem 8rem 3rem;
            }        
            .st-emotion-cache-1r4qj8v {
                color: rgb(116 64 64);
            }
            h1{
                color: rgb(158 64 107);
            }
            h3{
                color: rgb(226 227 55);
            }
            hr{
                margin: 0em 0px;
            }
            .st-emotion-cache-1gwvy71 {
                padding: 0px 1.5rem 1rem;
            }
            </style>
        """, unsafe_allow_html=True)
