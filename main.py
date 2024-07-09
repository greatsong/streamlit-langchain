import streamlit as st
import settings

st.title("📝 서울고 프로젝트 수업 전용 설PT")

config = settings.load_config()
if "api_key" in config:
    st.session_state.api_key = config["api_key"]

if "api_key2" in config:
    st.session_state.api_key2 = config["api_key2"]

main_text = st.empty()


api_key = st.text_input("🔑 새로운 OPENAI API Key", type="password")
api_key2 = st.text_input("🔑 새로운 Perplexity API Key", type="password")
save_btn = st.button("설정 저장", key="save_btn")

if save_btn:
    settings.save_config({"api_key": api_key})
    settings.save_config({"api_key2": api_key2})
    st.session_state.api_key = api_key
    st.session_state.api_key2 = api_key2
    st.write("설정이 저장되었습니다.")
