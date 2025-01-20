import streamlit as st


def main():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    is_logged_in = st.session_state.is_logged_in
    if not is_logged_in:
        pages = [st.Page("app/login.py", title="Авторизация", icon=":material/login:")]
    else:
        pages = [st.Page("app/account.py", title="Личный кабинет", icon=":material/account_circle:")]

    display_pages = st.navigation(pages)
    display_pages.run()


if __name__ == "__main__":
    main()
