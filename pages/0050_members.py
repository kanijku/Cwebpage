import streamlit as st
import pandas as pd
def main():

    st.title('集計するうえでのメンバー設定')
    st.markdown('#### このページでの操作によって後からメンバーの削除・追加を行うことができる')
    st.title("")

    memdf=pd.read_csv('data/memberdata.csv')
    num_mem=memdf.shape[0]
    st.markdown(f'### 現段階でのメンバー ({num_mem}人)')
    cols = st.columns(num_mem,vertical_alignment='top')
    for i in range(num_mem):
        with cols[i]:
            st.header(memdf.iloc[i]["name"])
            st.image(memdf.iloc[i]["icon"])

if __name__=='__main__':
    main()
