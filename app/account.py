import os
import base64

import time
import requests
import streamlit as st

import utils.data_processing as data_proc


@st.dialog("Добавить в избранное")
def bookmark():
    filename = st.text_input("Название")
    if st.button("Добавить", use_container_width=True):
        if not filename:
            st.error("Название не может быть пустым")
            st.stop()

        user_id = st.session_state.user_id
        audio_content = st.session_state.audio_content
        files = {"file_": audio_content}
        data_proc.load_api_data(url=f"users/{user_id}/upload_audio?filename={filename}", method="post", files=files)
        st.success("Сохранено")
        time.sleep(1)
        st.rerun()


@st.fragment
def show_music_sheet_converter():
    audio_content = st.session_state.audio_content
    uploaded_files = st.file_uploader("Выберите один или несколько файлов в порядке следования нотных листов", accept_multiple_files=True)
    if uploaded_files:
        if st.button("Преобразовать в аудиодорожку"):
            with st.spinner("Пожалуйста, подождите... данные обновляются."):
                try:
                    files = [("files", (f"{idx:03d}_{file_.name}", file_.read(), file_.type)) for idx, file_ in enumerate(uploaded_files, start=1)]
                    response = requests.post(f"{os.getenv('API_BASE_URL')}/app/process_music", files=files)
                    audio_content = response.content
                    st.session_state.audio_content = audio_content
                except Exception:
                    st.error("Ошибка при преобразовании файлов")
    if audio_content is not None:
        st.audio(audio_content, format="audio/wav")
        if st.button("Добавить в избранное", icon=":material/bookmark:"):
            bookmark()


@st.fragment
def show_users_music():
    user_id = st.session_state.user_id
    data = data_proc.load_api_data(url=f"users/{user_id}/my_music", method="get")

    if not data:
        st.caption("Здесь ничего нет... Но Вы можете добавить свою музыку, загрузив нотные листы")
        return

    with st.container(height=min(150 * len(data), 350)):
        for filename, content in sorted(data, key=lambda x: x[0]):
            st.subheader(filename)
            col1, col2 = st.columns([9, 1])
            with col1:
                audio_bytes = base64.b64decode(content)
                st.audio(audio_bytes)
            with col2:
                if st.button("", icon=":material/delete:", key=filename):
                    data_proc.load_api_data(url=f"users/{user_id}/my_music/delete?filename={filename}", method="put")
                    st.rerun()


def logout():
    st.session_state.is_logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()


def display():
    username = st.session_state.username
    st.title(f"Добро пожаловать, {username}!")
    st.session_state.audio_content = None
    show_music_sheet_converter()

    st.header("Моя музыка")
    show_users_music()

    if st.button("Выйти", icon=":material/logout:", type="primary"):
        logout()


display()
