import streamlit as st

import pandas as pd 


def main():
    st.title("TODO WEB APPLICTION !!")

    menu = ["Create","Read","Upadte","Delete"]
    choice = st.sidebar.selectbox("Menu",menu)
    


if __name__ == '__main__':
    main()