import streamlit as st
import pandas as pd

st.title("PA RAPTOR")
st.write("""
# My first app
Let's Go!
""")
 
df = pd.read_csv("Flex_24.csv")
st.dataframe(df)
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
