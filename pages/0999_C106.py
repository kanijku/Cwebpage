import streamlit as st
import pandas as pd
from pathlib import Path
import time
from functools import partial


with open('data/alps.txt', 'r', encoding='utf-8') as file:
    alplist = file.read()
    ALPLIST = list(alplist)
    if ALPLIST[0] != 'A':#utf-8のBOMを削除
        ALPLIST=ALPLIST[1:]

#######
PAGE_NAME='C106'
#######

def main():
    st.title(PAGE_NAME)
    file_path = Path(f'data/{PAGE_NAME}_data')
    if not file_path.exists():
        st.text('データがありません')
        st.button('merge and reset',on_click=countall)
    else:
        st.markdown('### 集計 ')
        dfall=pd.read_csv(f'data/{PAGE_NAME}_data/data_all.csv')
        edited_df=st.data_editor(dfall)
        btn_hanei=st.button("集計および反映",type='primary')

        if btn_hanei:
            change_data(edited_df)
    st.markdown('## 編集および追加')
    view_data()


    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('### メモおよび仕様')
    st.markdown('1. データはdataフォルダ内に保存されそれぞれのユーザーごとにファイルが作成されます。')
    st.markdown('2. サークル追加、サークル削除はこれらのユーザーごとのデータを書き換えるものです。')
    st.markdown('3. 集計および反映は全ユーザーのデータを集計し、data_all.csvに保存します。ただし、check コラムのデータはページ上の情報を優先し、data_all.csvの情報は上書きされます。')
def change_data(edited_df):
    countall() #data_all.csvはこの時点でcheckの情報をうしなう　
    dfall=pd.read_csv(f'data/{PAGE_NAME}_data/data_all.csv')

    
    merged = pd.merge(dfall, edited_df, on=["WorE", "alp", "number", "aorb"], how="left", suffixes=("_df1", "_df2"))
    dfall["check"] = merged["check"].fillna(False).astype(bool)
    dfall["count"] = merged["count_df1"]
    dfall.to_csv(f'data/{PAGE_NAME}_data/data_all.csv',index=False)

    st.text('データを更新しました')
    time.sleep(2)
    st.rerun()

def view_data():
    dfmem=pd.read_csv('data/memberdata.csv')

    with st.popover("Choose user"):
        name = st.radio('user',dfmem["name"])

    dfuser=pd.read_csv(f'data/{PAGE_NAME}_data/data_{name}.csv')
    st.markdown(f'### ユーザー:{name}')
    st.image(f'{dfmem.loc[dfmem["name"]==name,"icon"].values[0]}',width=100)
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

    @st.dialog("サークル削除")
    def delete_circle():
        index=st.number_input("削除する行番号",min_value=0)

        if st.button("削除"):
            dfuser=pd.read_csv(f'data/{PAGE_NAME}_data/data_{name}.csv')
            rmWorE=dfuser.iloc[index]["WorE"]
            rmalp=dfuser.iloc[index]["alp"]
            rmnumber=dfuser.iloc[index]["number"]
            rmaorb=dfuser.iloc[index]["aorb"]
            def btn_yes(dfuser):
                dfuser=dfuser.drop(index)
                dfuser.to_csv(f'data/{PAGE_NAME}_data/data_{name}.csv',index=False)
            def btn_no():
                st.text('キャンセルしました')
            st.text(f'{rmWorE} {rmalp} {rmnumber} {rmaorb} を削除しますか？')
                # 引数付きの関数をpartialを使って渡す
            btn_yes_with_args = partial(btn_yes, dfuser)
            btn_yes=st.button("はい",on_click=btn_yes_with_args)
            btn_no=st.button("いいえ",on_click=btn_no)

        
    
    btn_add=st.button("サークル追加")
    if btn_add:
        add_circle()
    if st.button("サークル削除"):
        delete_circle()
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

