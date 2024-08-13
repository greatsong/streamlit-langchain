import streamlit as st
import settings

st.title("📝쪼랩 원데이 클래스 전용 쫄PT")

config = settings.load_config()
if "api_key" in config:
    st.session_state.api_key = config["api_key"]
    st.write(f'사용자 입력 API키 : {st.session_state.api_key[-5:]}')
else : 
    st.session_state.api_key = st.secrets["openai_api_key"]
    st.write(f'API키 : {st.secrets["openai_api_key"][-5:]}')
main_text = st.empty()


api_key = st.text_input("🔑 새로운 OPENAI API Key", type="password")
save_btn = st.button("설정 저장", key="save_btn")

if save_btn:
    settings.save_config({"api_key": api_key})
    st.session_state.api_key = api_key
    st.write("설정이 저장되었습니다.")
