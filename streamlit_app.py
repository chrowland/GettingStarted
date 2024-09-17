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
st.button("Commit Changes")
st.info(
    """
    Outputs table. Displays calculations from the last PA Raptor run using inputs table above. Validate.
    To change outputs, revise inputs in table above and commit changes. Changes to inputs will affect outputs.
    """
)
#Calculate the output table
dfT=df.T
output=pd.DataFrame()
output['Flex Connections']=dfT['PA Connections']*dfT['Flex SOV']
output['Flex Transactions']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']
output['Gross Revenue']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']*dfT['Referral Fee']
output['Accrual']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']*dfT['Referral Fee']*(1-dfT['Collection'])
output=output.T
st.dataframe(output)
st.button("Push Scenario to Hive")

st.title("Monthly Connections")
st.line_chart(df.iloc[0,:])

st.data_editor(df)
