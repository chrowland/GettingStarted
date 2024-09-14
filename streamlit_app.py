import streamlit as st

st.title("🎈 My new app")
st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("my_data.csv")
st.line_chart(df)
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
