import streamlit as st
import pandas as pd
import os
import time
with open('data/alps.txt', 'r', encoding='utf-8') as file:
    alplist = file.read()
    ALPLIST = list(alplist)
PAGE_NAME='C105'

def main():
    st.title(PAGE_NAME)
    if not os.path.isfile(f'data/{PAGE_NAME}_data/data_all.csv'):
        st.text('データがありません')
        st.button('merge and reset',on_click=countall)
    else:
        st.markdown('### 集計 ')
        dfall=pd.read_csv(f'data/{PAGE_NAME}_data/data_all.csv')
        edited_df=st.data_editor(dfall)
        btn_hanei=st.button("反映")

        if btn_hanei:
            change_data(edited_df)
    st.markdown('## 編集および追加')
    view_data()

    
def syuukei_main():
    st.markdown('### 集計 ')
    #btn_countall=st.button('集計')
    dfall=pd.read_csv(f'data/{PAGE_NAME}_data/data_all.csv')
    edited_df=st.data_editor(dfall)
    #上書き
    edited_df.to_csv(f'data/{PAGE_NAME}_data/data_all.csv',index=False)
    #st.rerun(scope='fragment')
    btn_hanei=st.button("反映")
    st.button('merge and reset',on_click=countall)
    if btn_hanei:
        change_data(edited_df)
def change_data(edited_df):
    edited_df.to_csv(f'data/{PAGE_NAME}_data/data_all.csv',index=False)
    st.text('データを更新しました')
    st.rerun()

def view_data():
    dfmem=pd.read_csv('data/memberdata.csv')

    with st.popover("Choose user"):
        name = st.radio('user',dfmem["name"])

    dfuser=pd.read_csv(f'data/{PAGE_NAME}_data/data_{name}.csv')
    st.markdown(f'### ユーザー:{name}')
    st.dataframe(dfuser)
    add_data(name)

def add_data(name):
    @st.dialog("サークル追加")

    def add_circle():
        WorE=st.radio("東か西",["東","西"])
        alp=st.selectbox("アルファベット",ALPLIST)
        number=st.number_input("数字",min_value=1,max_value=100)
        aorb=st.radio("aかbか",["a","b","ab"])
        count=st.number_input("部数",min_value=1)

        if st.button("追加"):
            adddf(name,WorE,alp,number,aorb,count)
            st.text('追加しました')
            st.rerun()
    
    btn_add=st.button("サークル追加")
    if btn_add:
        add_circle()
def adddf(name,WorE,alp,number,aorb,count):
    try:
        df=pd.read_csv(f'data/{PAGE_NAME}_data/data_{name}.csv')
    except:
        df=pd.DataFrame(columns=["WorE","alp","number","aorb","count"])

    dftmp=pd.DataFrame({"WorE":[WorE],"alp":[alp],"number":[number],"aorb":[aorb],"count":[count]})
    df=pd.concat([df,dftmp])
    df.to_csv(f'data/{PAGE_NAME}_data/data_{name}.csv',index=False)
def countall():
    datainit()
    memdf=pd.read_csv('data/memberdata.csv')
    num_mem=memdf.shape[0]
    df=pd.DataFrame()
    for i in range(num_mem):
        memname=memdf.iloc[i]["name"]
        dftmp=pd.read_csv(f'data/{PAGE_NAME}_data/data_{memname}.csv')
        dftmp["user"]=memname

        df=pd.concat([df,dftmp])
    result=df.groupby(["WorE","alp","number","aorb"],as_index=False)["count"].sum()
    result["check"]=False
    result.to_csv(f'data/{PAGE_NAME}_data/data_all.csv',index=False)

    
def datainit():
    #ここではメンバー全員のデータフレームを作製する。ディレクトリ内にファイルがなかった場合のみcsvを作成する
    memdf=pd.read_csv('data/memberdata.csv')
    num_mem=memdf.shape[0]

    for i in range(num_mem):
        memname=memdf.iloc[i]["name"]
        try:
            dftmp=pd.read_csv(f'data/{PAGE_NAME}_data/data_{memname}.csv')
        except:
            dftmp=pd.DataFrame(columns=["WorE","alp","number","aorb","count"])
            dftmp.to_csv(f'data/{PAGE_NAME}_data/data_{memname}.csv',index=False)
        
if __name__=='__main__':
    main()

