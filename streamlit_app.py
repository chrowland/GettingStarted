import streamlit as st
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="RAPTOR - PA",
    page_icon=":eagle:",  # This is an emoji shortcode. Could be a URL too.
    layout="wide"
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

df_inputs = pd.read_csv("PARA_ex_inputs.csv")
df_inputs.set_index('Input Metric', inplace=True)
#st.data_editor(df_inputs)
df=st.data_editor(df_inputs)
if st.checkbox("Show Equations"):
    st.write("Flex Connections = PA Connections X Flex SOV")
    st.write("Flex Transactions = PA Connections X Flex SOV X Cxn Conversion")
    st.write("Gross Revenue = PA Connections X Flex SOV X Cxn Conversion X Referral Fee")
    st.write("Accrual = Gross Revenue X (1 - Collection)")
else:
    st.write("")
st.info(
    """
    Outputs table. Displays calculations from the last PA Raptor run using inputs table above. Validate.
    To change outputs, revise inputs in table above and commit changes. Changes to inputs will affect outputs.
    """
)
#Calculate Baseline
df_inputsT=df_inputs.T
Baselines=pd.DataFrame()
Baselines['Flex Connections']=df_inputsT['PA Connections']*df_inputsT['Flex SOV']
Baselines['Flex Transactions']=df_inputsT['PA Connections']*df_inputsT['Flex SOV']*df_inputsT['Cxn Conversion W/ Seasonality & Mix']
Baselines['Gross Revenue']=df_inputsT['PA Connections']*df_inputsT['Flex SOV']*df_inputsT['Cxn Conversion W/ Seasonality & Mix']*df_inputsT['Referral Fee']
Baselines['Accrual']=df_inputsT['PA Connections']*df_inputsT['Flex SOV']*df_inputsT['Cxn Conversion W/ Seasonality & Mix']*df_inputsT['Referral Fee']*(1-df_inputsT['Collection'])

#Calculate the dynamic output table
dfT=df.T
output=pd.DataFrame()
output['Flex Connections']=dfT['PA Connections']*dfT['Flex SOV']
output['Flex Transactions']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']
output['Gross Revenue']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']*dfT['Referral Fee']
output['Accrual']=dfT['PA Connections']*dfT['Flex SOV']*dfT['Cxn Conversion W/ Seasonality & Mix']*dfT['Referral Fee']*(1-dfT['Collection'])
output=output.T
st.dataframe(output)
st.button("Push Scenario to Hive")
chartdf=pd.DataFrame[Baselines['Gross Revenue'],output.T['Gross Revenue']]
st.title("Gross Revenue")

st.line_chart(chartdf)
#output.iloc[2,:]
st.title("Sensitivities")
