import streamlit as st
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="RAPTOR - PA",
    page_icon=":eagle:",  # This is an emoji shortcode. Could be a URL too.
)
st.title("PA RAPTOR")
st.write("""
# Validation Studio
""")

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

df = pd.read_csv("Flex_24.csv")
df.set_index('metric', inplace=True)
st.dataframe(df)
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.title("Monthly Leads")
st.line_chart(df.iloc[0,:])
