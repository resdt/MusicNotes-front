import os
import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL")


def load_api_data(url: str, method: str, json: dict = None, files: dict = None):
    with st.spinner("Пожалуйста, подождите... данные обновляются."):
        try:
            full_url = f"{API_BASE_URL}/{url}"
            if method == "post":
                response = requests.post(full_url, json=json, files=files) if files else requests.post(full_url, json=json)
            elif method == "get":
                response = requests.get(full_url)
            elif method == "put":
                response = requests.put(full_url, json=json, files=files) if files else requests.put(full_url, json=json)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            st.error("Ошибка подключения к серверу")
            st.stop()
