import streamlit as st

st.title("🎈 My new app")
st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("Flex_24.csv")
st.dataframe(df)
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
