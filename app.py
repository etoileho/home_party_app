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
st.balloons()

st.header(':blue[〇メニュー表]')
# GitHubから非公開リポジトリ内の画像を取得
image_path = PATH + "drink_menu.jpg"  # PATH変数を使用して正しい画像のパスを指定
content_file = repo.get_contents(image_path, ref="main")  # 'ref'にはブランチ名を指定（デフォルトは'main'）
image_data = base64.b64decode(content_file.content)  # base64エンコードされた内容をデコード
image_bytes = BytesIO(image_data)  # BytesIOオブジェクトに変換

# Streamlitで画像を表示
st.image(image_bytes, caption='ドリンクメニュー')

st.header(':blue[〇注文フォーム]')

with st.form("order_form"):
    name = st.text_input('お名前')
    drink = st.selectbox('ドリンクを選択してください', ['ダージリンクーラー','セイロンオレンジスクリューズ','バイオレットジンジャー','オレンジムーン','クランベリージンジャーマティーニ','チェリースピリッツ','カシスオレンジ','カシスソーダ','セイロンソーダ','クランベリーソーダ','ハイボール','ジンジャーハイ','家主のきまぐれ','リクエスト(下の欄に記載)'])
    picture = st.camera_input("パーティへの気持ちを写真で表現して！！")
    comments = st.text_area('特別な要望またはひとこと！')
    submit_button = st.form_submit_button('注文')
    
if submit_button:
    order_details = f"名前: {name}\nドリンク: {drink}\n特別な要望またはひとこと: {comments}"
    save_order_to_github(order_details, picture, name)
