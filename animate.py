import streamlit as st
import streamlit.components.v1 as components



def css():
    st.markdown(
        """
        <style>
        .fade-in {
            animation: fadeIn 2s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .slide-in {
            animation: slideIn 1.5s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        .bounce-in {
            animation: bounceIn 1.5s ease;
        }
        @keyframes bounceIn {
            from {
                opacity: 0;
                transform: scale3d(.3, .3, .3);
            }
            50% {
                opacity: 1;
                transform: scale3d(1.05, 1.05, 1.05);
            }
            to {
                transform: scale3d(1, 1, 1);
            }
        }
        .zoom-in {
            animation: zoomIn 1s ease;
        }
        @keyframes zoomIn {
            from {
                opacity: 0;
                transform: scale(0);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        .glow {
            animation: glow 1.5s infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }
            to {
                text-shadow: 0 0 20px rgba(255, 255, 255, 1);
            }
        }
        </style>
        """, unsafe_allow_html=True
    )