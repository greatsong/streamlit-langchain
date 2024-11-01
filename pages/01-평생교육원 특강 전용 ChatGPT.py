import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.callbacks.base import BaseCallbackHandler
import os
import pickle
import datetime
import settings


# API KEY 를 설정합니다.
if "api_key" not in st.session_state:
    config = settings.load_config()
    if "api_key" in config:
        st.session_state.api_key = settings.load_config()["api_key"]
    else:
        st.session_state.api_key = ""

st.title("서울대 평생교육원 프로젝트 수업 전용 쫄PT")

st.markdown(
    f"""API KEY
    `{st.session_state.api_key[:-15] + '***************'}`
    """
)


if "history" not in st.session_state:
    st.session_state.history = []

if "user" not in st.session_state:
    st.session_state.user = []

if "ai" not in st.session_state:
    st.session_state.ai = []


def add_history(role, content):
    if role == "user":
        st.session_state.user.append(content)
    elif role == "ai":
        st.session_state.ai.append(content)


model_name = st.empty()
tab1, tab2 = st.tabs(["Chat", "Settings"])


class StreamCallback(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.full_text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.full_text += token
        self.container.markdown(self.full_text)


# ChatOpenAI 객체를 생성합니다.
llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    callbacks=[StreamCallback(st.empty())],
    api_key=st.session_state.api_key,
)

# ConversationChain 객체를 생성합니다.
conversation = ConversationChain(
    llm=llm, verbose=False, memory=ConversationBufferMemory()
)

prompt_preset = "이 강의는 서울대 평생교육원에서 열린 데이터 분석 기초 과정이야. 수강생 선생님들이 물어보시는 것에 친절하게 답변해주고, 특히 이모지를 풍부하게 써서 MBTI ENFP 느낌으로 답변을 작성해주렴!"

prompt_input = prompt_preset # 수정
#prompt_input = tab2.text_area("Prompt", value=prompt_preset)


def create_prompt_template(prompt_input):
    prompt_template = PromptTemplate.from_template(
        """
{custom_prompt}

HISTORY:
{history}

QUESTION:
{input}

ANSWER:

"""
    )
    prompt_template = prompt_template.partial(custom_prompt=prompt_input)
    return prompt_template


if prompt_input:
    prompt_template = create_prompt_template(prompt_input)
    conversation.prompt = prompt_template

model_input = tab2.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o"], index=1)

if model_input:
    settings.save_config({"model": model_input})
    llm.model_name = model_input
    model_name.markdown(f"#### {model_input}")


def print_history():
    for i in range(len(st.session_state.ai)):
        tab1.chat_message("user").write(st.session_state["user"][i])
        tab1.chat_message("ai").write(st.session_state["ai"][i])

print_history()

if prompt := st.chat_input():
    add_history("user", prompt)

    tab1.chat_message("user").write(prompt)
    with tab1.chat_message("assistant"):
        msg = st.empty()
        llm.callbacks[0].container = msg
        for user, ai in st.session_state.history:
            conversation.memory.save_context(inputs={"human": user}, outputs={"ai": ai})
        response = conversation.invoke(
            {"input": prompt, "history": st.session_state.history}
        )
        st.session_state.history.append((prompt, response["response"]))
        add_history("ai", response["response"])
