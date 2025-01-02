import streamlit as st
import pandas as pd

df=pd.read_csv('./data.csv',index_col='WorE')
st.dataframe(df)