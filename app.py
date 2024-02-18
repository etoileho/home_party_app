import streamlit as st
from github import Github
import datetime
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
PATH = os.getenv('GITHUB_PATH', '')

# GitHubに接続
g = Github(ACCESS_TOKEN)
repo = g.get_repo(REPO_NAME)

def save_order_to_github(order_details):
    try:
        # 現在の日時をファイル名に使用
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
        # コミットメッセージ
        commit_message = f"New order: {filename}"
        # GitHubにファイルを作成（新しい注文を保存）
        repo.create_file(PATH + filename, commit_message, order_details)
        st.success('注文が成功しました！')
    except Exception as e:
        st.error(f'注文の保存中にエラーが発生しました: {e}')

# ストリームリットUI
st.title('ホームパーティーメニュー注文フォーム')

with st.form("order_form"):
    name = st.text_input('名前')
    drink = st.selectbox('ドリンクを選択してください', ['ドリンク1', 'ドリンク2', 'ドリンク3'])
    comments = st.text_area('特別な要望')
    submit_button = st.form_submit_button('注文')

if submit_button:
    order_details = f"名前: {name}\nドリンク: {drink}\n特別な要望: {comments}"
    save_order_to_github(order_details)
