import streamlit as st
from pathlib import Path
import shutil
import zipfile
import io

def main():
    st.title('管理者ページ')
    st.markdown('#### このページは管理者ページです。')
    st.markdown('#### ページのソースコードを変更してgithub上のデータを最新にするとサイト上で変更したデータはすべて上書きされてしまうためにサイト上でユーザーが書き換えた最新のデータすべてをダウンロードするためのページです。')


    # ダウンロード対象のディレクトリ
    directory_to_zip = Path("data")  # 圧縮したいディレクトリを指定

    # ZIPファイルを作成する関数
    def create_zip_with_encoding(directory):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in directory.rglob("*"):  # ディレクトリ内のすべてのファイル・サブディレクトリを取得
                if file_path.is_file():
                    # ファイルを読み取りUTF-8でエンコード
                    with file_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                        # BOMを付加
                        bom_content = "\ufeff" + content
                    # メモリ上にエンコード済みのデータを書き込む
                    zip_file.writestr(str(file_path.relative_to(directory)), bom_content)
        zip_buffer.seek(0)  # メモリの先頭に移動
        return zip_buffer

    # ZIPファイル作成とダウンロードボタン
    zip_buffer = create_zip_with_encoding(directory_to_zip)
    st.download_button(
        label="Download Directory as ZIP",
        data=zip_buffer,
        file_name="directory.zip",
        mime="application/zip"
    )

    st.markdown("ダウンロード時にエンコードを utf-8 にしています。また、そのうえ、エクセル上でcsvを表示することを想定して、BOMを付加しています。そのため特にalps.txtのようなテキストファイルから文字列をリストとして読み込むと先頭が文字データでなくなっていることがあります。")
if __name__=='__main__':
    main()
