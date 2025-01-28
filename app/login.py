import streamlit as st
import hashlib
import time

import utils.data_processing as data_proc


@st.dialog("Регистрация")
def sign_up():
    def change_input_state():
        st.session_state.username_changed = True

    username = st.text_input("Введите имя пользователя", on_change=change_input_state)
    valid_username = st.session_state.valid_username
    if username and st.session_state.username_changed:
        st.session_state.username_changed = False
        data = data_proc.load_api_data(url=f"app/check_username?username={username}", method="post")
        valid_username = data["validity"]
        st.session_state.valid_username = valid_username
    if not valid_username and username:
        st.error("Имя пользователя уже используется")

    password = st.text_input("Введите пароль", type="password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if st.button("Зарегистрироваться", use_container_width=True):
        if all([username,
                password,
                hashed_password,
                valid_username]):
            try:
                json = {"username": username, "hashed_password": hashed_password}
                data_proc.load_api_data(url="app/sign_up", method="post", json=json)
                st.success("Вы успешно зарегистрировались")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                print(e)
                st.error("Ошибка добавления пользователя")
        else:
            st.error("Не все поля заполнены")


def display():
    st.title("MusicNotes")
    with st.form("login_form"):
        username = st.text_input("Логин").strip().lower()
        password = st.text_input("Пароль", type="password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if st.form_submit_button("Войти"):
            json = {"username": username, "hashed_password": hashed_password}
            data = data_proc.load_api_data(url="app/login", method="post", json=json)

            if data["success"]:
                st.session_state.user_id = data["user_id"]
                st.session_state.username = data["username"]
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Неправильный логин или пароль")

        if st.form_submit_button("Зарегистрироваться", type="primary"):
            st.session_state.valid_username = False
            st.session_state.username_changed = False
            sign_up()


display()
