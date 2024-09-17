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
    Inputs table. Displays inputs to last PA Raptor run. Validate and overwrite to see impacts of revision.
    And don't forget to commit your changes when you're done.
    """
)

df = pd.read_csv("PARA_ex_inputs.csv")
df.set_index('Input Metric', inplace=True)
st.dataframe(df)

#Calculate the output table
outputs=pd.DataFrame()
outputs

st.title("Monthly Connections")
st.line_chart(df.iloc[0,:])
