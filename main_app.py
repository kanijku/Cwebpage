import streamlit as st
import re
from pathlib import Path

st.title('赤ちゃんのおへや')
st.caption('このページは赤ちゃんのお部屋です。')
st.caption('基本的にはコミケに関する情報を共有するためのページです。')
st.text('')
st.text('')
st.text('リンク')
# 対象のディレクトリパス
directory = Path('pages')

# ディレクトリ内のファイル一覧を取得
file_names = [f.name for f in directory.iterdir() if f.is_file()]

# 結果を表示
for filerow in file_names:
    print(filerow)
    file=filerow.strip('.py')
    file=re.sub(r'^\d{4}_',' ',file)
    #st.page_link(f"pages/{filerow}", label=file)
    #st.page_link(f"main_app.py",label="trest")
    st.page_link(f"./pages/{filerow}",label=f"{file}")
    #st.page_link(f"./pages/0999C106.py",label=file)
st.markdown('## news')
st.text('[2025/1/2]赤ちゃんのお部屋 始動！')