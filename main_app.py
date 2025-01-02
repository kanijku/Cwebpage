import streamlit as st
from PIL import Image

st.title('web page')
st.caption('This is a main page')

image=Image.open('./figures/jikkou_button.jpg')
st.image(image, caption='実行ボタン', width=200)