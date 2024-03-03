import streamlit as st
from github import Github
import datetime
import os
import base64
from io import BytesIO

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
PATH = os.getenv('GITHUB_PATH', '')

# GitHubに接続
g = Github(ACCESS_TOKEN)
repo = g.get_repo(REPO_NAME)

def save_order_to_github(order_details, picture=None, name=""):
    try:
        # 名前を安全なファイル名に変換（スペースや特殊文字をアンダースコアに置換）
        safe_name = "".join([c if c.isalnum() else "_" for c in name])

        # 現在の日時と名前をファイル名の一部として使用
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        details_filename = f"{safe_name}_{timestamp}.txt"
        image_filename = f"{safe_name}_{timestamp}.jpg"  # 画像ファイル名

        # 注文の詳細をテキストファイルとして保存
        commit_message_details = f"New order: {details_filename}"
        repo.create_file(PATH + details_filename, commit_message_details, order_details)

        # 画像が提供されている場合、画像形式で保存
        if picture:
            # Streamlitが提供するBytesIOオブジェクトから画像データを取得
            picture_bytes = picture.getvalue()

            # GitHubに画像ファイルとして保存
            commit_message_image = f"New image: {image_filename}"
            repo.create_file(PATH + image_filename, commit_message_image, picture_bytes, branch="main")

        st.success('注文が成功しました！')
    except Exception as e:
        st.error(f'注文の保存中にエラーが発生しました: {e}')



# ストリームリットUI
st.title(':orange[保科家ホムパ！]')

st.header(':blue[〇日程について]')
st.balloons()
st.caption('開催日：3月16日　(時間は追って連絡します、ランチタイムからの予定です)')
st.caption('参加料は無し、みんなで食べ物を持ち寄ってやります！')
st.caption('ウェルカムドリンクを作るので、何を飲みたいか下の注文フォームで注文してください！')

st.header(':blue[〇メニュー表]')
st.image("https://github.com/etoileho/home_party/blob/main/drink_menu.jpg")

st.header(':blue[〇注文フォーム]')

with st.form("order_form"):
    name = st.text_input('お名前')
    drink = st.selectbox('ドリンクを選択してください', ['ダージリンクーラー', 'バイオレットジンジャー', 'オレンジムーン', 'チェリースプリッツ'])
    picture = st.camera_input("パーティへの気持ちを写真で")
    comments = st.text_area('特別な要望またはひとこと！')
    submit_button = st.form_submit_button('注文')
    
if submit_button:
    order_details = f"名前: {name}\nドリンク: {drink}\n特別な要望またはひとこと: {comments}"
    save_order_to_github(order_details, picture, name)
