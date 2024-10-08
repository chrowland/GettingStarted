import streamlit as st
import pandas as pd
import altair as alt

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
    """
)

df_inputs = pd.read_csv("PARA_ex_inputs.csv")
df_inputs.set_index('Input Metric', inplace=True)
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
Final_Frame=df.T.join(output.T,how='left')

chartdf=pd.DataFrame()

Target = st.selectbox(
    "Target Output Variable",
    ("Gross Revenue", "Flex Transactions", "Flex Connections", "Accrual"),
)

chartdf['Baseline']=Baselines[Target]
chartdf['Scenario']=output.T[Target]
chartdf['Difference']=chartdf['Scenario']-chartdf['Baseline']
st.title(Target)

st.bar_chart(chartdf.iloc[:,0:2],stack=False)
st.write(chartdf.T)

with st.form("scenario_name"):
    scenario_name=st.text_input('Name your Scenario:','Danny\'s super cool scenario')
    st.form_submit_button('Submit')
st.download_button(f"Download {scenario_name}",Final_Frame.T.to_csv(),f"{scenario_name}.csv",use_container_width=True)



st.title("Sensitivities")
sensitivities=pd.DataFrame({'Metric':['Flex SOV', 'Referral Fee', 'Collection', 'PA Connection'],'Impact': [.04,.05,.02,.01]})


st.info(
    """
   The values shown in the X axis of the table below express the sensitivity of the output variable (in this case Gross Revenue) to a 1% change in the input variable on the y axis.
   That is, each input variable is multiplied by 1.01 (a 1% increase) and the percentage change in Gross Revenue is calculated and shown in the chart.
   The greater the variable's bar in the chart below, the greater the impact it has on Gross Revenue
    """
)

chart=alt.Chart(sensitivities.sort_values('Impact',ascending=False)).mark_bar().encode(
    x='Impact:Q',
    y='Metric:N',
    color='Metric:N'
)
st.altair_chart(chart)

#st.dataframe(sensitivities.sort_values('Impact',ascending=False))
st.title("Risks and Opportunities")
st.write("Risks and Opportunities identified for this quarter are listed below. Check or uncheck specific R&Os to include or exclude them from your scenario. The R&Os that were included in the PA Raptor base case are selected by default")
RO_df = pd.DataFrame(
    {
        "R&O": ["Enhanced Market Expansion", "Marketing Spend Ramp UP", "FUB Bundle", "Spam Remediation"],
        "Include?": [False, True, False, True],
    }
)

st.data_editor(
    RO_df,
    column_config={
        "favorite": st.column_config.CheckboxColumn(
            "Include?",
            help="Select R&Os to include in forecast",
            default=False,
        )
    },
    disabled=["R&O"],
    hide_index=True,
)

