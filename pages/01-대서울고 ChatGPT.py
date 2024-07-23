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

st.title("대서울고 VPython 프로젝트 수업 전용 설PT")

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

prompt_preset = """이와 같은 형식의 데이터가 age.csv에 저장되어 있어. 이 내용을 참고해서 질문에 답해줘
행정구역	2024년06월_계_총인구수	2024년06월_계_연령구간인구수	2024년06월_계_0세	2024년06월_계_1세	2024년06월_계_2세	2024년06월_계_3세	2024년06월_계_4세	2024년06월_계_5세	2024년06월_계_6세	2024년06월_계_7세	2024년06월_계_8세	2024년06월_계_9세	2024년06월_계_10세	2024년06월_계_11세	2024년06월_계_12세	2024년06월_계_13세	2024년06월_계_14세	2024년06월_계_15세	2024년06월_계_16세	2024년06월_계_17세	2024년06월_계_18세	2024년06월_계_19세	2024년06월_계_20세	2024년06월_계_21세	2024년06월_계_22세	2024년06월_계_23세	2024년06월_계_24세	2024년06월_계_25세	2024년06월_계_26세	2024년06월_계_27세	2024년06월_계_28세	2024년06월_계_29세	2024년06월_계_30세	2024년06월_계_31세	2024년06월_계_32세	2024년06월_계_33세	2024년06월_계_34세	2024년06월_계_35세	2024년06월_계_36세	2024년06월_계_37세	2024년06월_계_38세	2024년06월_계_39세	2024년06월_계_40세	2024년06월_계_41세	2024년06월_계_42세	2024년06월_계_43세	2024년06월_계_44세	2024년06월_계_45세	2024년06월_계_46세	2024년06월_계_47세	2024년06월_계_48세	2024년06월_계_49세	2024년06월_계_50세	2024년06월_계_51세	2024년06월_계_52세	2024년06월_계_53세	2024년06월_계_54세	2024년06월_계_55세	2024년06월_계_56세	2024년06월_계_57세	2024년06월_계_58세	2024년06월_계_59세	2024년06월_계_60세	2024년06월_계_61세	2024년06월_계_62세	2024년06월_계_63세	2024년06월_계_64세	2024년06월_계_65세	2024년06월_계_66세	2024년06월_계_67세	2024년06월_계_68세	2024년06월_계_69세	2024년06월_계_70세	2024년06월_계_71세	2024년06월_계_72세	2024년06월_계_73세	2024년06월_계_74세	2024년06월_계_75세	2024년06월_계_76세	2024년06월_계_77세	2024년06월_계_78세	2024년06월_계_79세	2024년06월_계_80세	2024년06월_계_81세	2024년06월_계_82세	2024년06월_계_83세	2024년06월_계_84세	2024년06월_계_85세	2024년06월_계_86세	2024년06월_계_87세	2024년06월_계_88세	2024년06월_계_89세	2024년06월_계_90세	2024년06월_계_91세	2024년06월_계_92세	2024년06월_계_93세	2024년06월_계_94세	2024년06월_계_95세	2024년06월_계_96세	2024년06월_계_97세	2024년06월_계_98세	2024년06월_계_99세	2024년06월_계_100세 이상
서울특별시  (1100000000)	9366283 	9366283 	37461 	39642 	41067 	43089 	45114 	48661 	52273 	57940 	64865 	67342 	65963 	71062 	72255 	73959 	69868 	71228 	77444 	73919 	72665 	79480 	89507 	92064 	102695 	125816 	135982 	141632 	154772 	160863 	166768 	166015 	167171 	168455 	164246 	147933 	140841 	136145 	127881 	127372 	128071 	125656 	134076 	141507 	150272 	150216 	149164 	135300 	132215 	132721 	132955 	141421 	152392 	156235 	158824 	163793 	155818 	158920 	142128 	134938 	135110 	137553 	127021 	142856 	132100 	152515 	147242 	134623 	129339 	121167 	115921 	120430 	95608 	92723 	88288 	70574 	79594 	74294 	74840 	73383 	50667 	54382 	50631 	54595 	52005 	40376 	35221 	31898 	26309 	22916 	19390 	15590 	12042 	9350 	7375 	5270 	4361 	3474 	2428 	1666 	918 	650 	1511 
서울특별시 종로구 (1111000000)	139189 	139189 	385 	423 	480 	460 	543 	523 	605 	689 	805 	793 	791 	933 	884 	963 	883 	923 	1071 	982 	986 	1205 	1415 	1471 	1672 	2078 	2368 	2440 	2422 	2562 	2542 	2470 	2410 	2483 	2338 	2057 	1874 	1761 	1680 	1670 	1600 	1691 	1765 	1845 	1995 	2044 	2000 	1771 	1776 	1836 	1773 	1971 	2248 	2348 	2478 	2577 	2504 	2548 	2305 	2249 	2190 	2197 	2166 	2367 	2130 	2503 	2215 	2086 	1945 	1856 	1815 	1858 	1422 	1423 	1337 	993 	1180 	1114 	1219 	1144 	853 	994 	885 	980 	979 	814 	703 	636 	531 	475 	398 	330 	262 	198 	163 	114 	89 	75 	56 	45 	24 	18 	43 
서울특별시 종로구 청운효자동(1111051500)	11190 	11190 	47 	32 	41 	50 	47 	49 	53 	81 	83 	78 	78 	108 	103 	113 	94 	119 	100 	131 	98 	103 	113 	118 	92 	127 	128 	153 	135 	168 	163 	167 	162 	182 	174 	148 	130 	144 	144 	129 	132 	149 	156 	151 	195 	204 	219 	184 	162 	173 	181 	197 	219 	210 	203 	180 	207 	220 	183 	162 	181 	145 	156 	153 	148 	166 	162 	145 	136 	113 	134 	119 	99 	111 	98 	78 	98 	84 	89 	96 	72 	86 	73 	86 	78 	60 	57 	51 	50 	39 	34 	23 	27 	20 	12 	12 	5 	6 	5 	3 	1 	1 	6 
서울특별시 종로구 사직동(1111053000)	8977 	8977 	19 	31 	42 	31 	39 	46 	52 	55 	62 	73 	59 	58 	68 	62 	43 	67 	73 	64 	55 	75 	83 	61 	76 	78 	101 	115 	112 	132 	124 	161 	162 	166 	186 	170 	136 	123 	122 	128 	123 	129 	160 	157 	149 	157 	110 	126 	126 	160 	118 	137 	140 	149 	143 	165 	175 	157 	143 	136 	124 	128 	129 	140 	126 	150 	132 	125 	129 	115 	110 	93 	87 	80 	73 	63 	69 	71 	76 	59 	58 	70 	64 	67 	58 	56 	50 	50 	53 	44 	25 	35 	22 	16 	10 	14 	8 	13 	2 	4 	2 	1 	6 
서울특별시 종로구 삼청동(1111054000)	2226 	2226 	4 	6 	7 	7 	6 	6 	13 	7 	15 	10 	13 	14 	14 	15 	17 	14 	17 	18 	20 	15 	16 	10 	19 	22 	25 	25 	36 	29 	23 	33 	30 	31 	28 	23 	32 	38 	24 	29 	26 	33 	21 	41 	30 	38 	41 	24 	30 	29 	25 	26 	28 	33 	35 	32 	35 	34 	36 	28 	38 	36 	33 	34 	45 	38 	42 	49 	36 	32 	34 	40 	29 	34 	29 	9 	28 	27 	30 	21 	22 	21 	18 	20 	28 	14 	15 	11 	13 	10 	13 	8 	6 	7 	6 	4 	5 	0 	2 	1 	0 	0 	2 
서울특별시 종로구 부암동(1111055000)	9042 	9042 	20 	27 	28 	21 	31 	27 	49 	51 	59 	65 	60 	92 	75 	71 	76 	66 	98 	71 	90 	93 	100 	78 	91 	97 	103 	121 	106 	108 	122 	117 	131 	147 	136 	124 	110 	107 	91 	104 	122 	105 	134 	113 	132 	148 	165 	129 	141 	130 	123 	150 	169 	183 	161 	166 	174 	172 	157 	141 	145 	158 	157 	145 	119 	159 	148 	142 	133 	115 	125 	131 	93 	89 	73 	68 	77 	72 	90 	71 	68 	58 	55 	57 	65 	45 	54 	43 	35 	38 	29 	22 	14 	11 	9 	19 	3 	9 	8 	4 	4 	1 	3 
서울특별시 종로구 평창동(1111056000)	17262 	17262 	50 	72 	72 	84 	100 	89 	111 	104 	145 	145 	143 	152 	125 	185 	134 	149 	173 	166 	136 	166 	166 	158 	170 	215 	193 	200 	173 	237 	208 	233 	214 	221 	220 	183 	179 	181 	197 	198 	219 	225 	207 	239 	272 	282 	267 	232 	225 	229 	223 	247 	311 	302 	315 	333 	296 	349 	315 	308 	300 	267 	293 	315 	306 	339 	289 	278 	265 	275 	235 	236 	203 	181 	148 	126 	122 	131 	159 	140 	105 	117 	103 	94 	100 	96 	82 	81 	80 	60 	61 	46 	51 	27 	33 	12 	12 	14 	8 	9 	3 	5 	12 
서울특별시 종로구 무악동(1111057000)	7938 	7938 	25 	36 	32 	49 	48 	45 	58 	75 	83 	66 	79 	92 	97 	103 	106 	96 	95 	98 	72 	89 	92 	88 	89 	89 	81 	75 	84 	80 	63 	78 	72 	81 	90 	63 	84 	69 	80 	90 	91 	89 	124 	132 	126 	125 	133 	123 	110 	139 	134 	135 	163 	150 	178 	188 	167 	141 	117 	93 	112 	124 	109 	135 	119 	132 	116 	104 	105 	100 	87 	108 	72 	71 	75 	50 	63 	66 	65 	55 	43 	52 	39 	45 	60 	59 	37 	41 	28 	25 	20 	20 	11 	14 	6 	4 	3 	5 	2 	2 	0 	0 	4 
서울특별시 종로구 교남동(1111058000)	9682 	9682 	51 	56 	60 	62 	81 	83 	77 	89 	94 	82 	76 	85 	67 	70 	76 	83 	77 	77 	86 	81 	70 	78 	77 	113 	111 	105 	145 	123 	127 	143 	137 	145 	138 	131 	149 	141 	129 	161 	135 	142 	161 	164 	200 	189 	173 	161 	165 	158 	153 	165 	169 	225 	168 	184 	173 	175 	141 	175 	114 	118 	135 	126 	97 	151 	110 	131 	123 	105 	104 	112 	84 	77 	78 	77 	90 	73 	59 	72 	55 	49 	50 	51 	58 	45 	47 	30 	26 	34 	23 	21 	11 	9 	4 	7 	3 	5 	1 	3 	1 	1 	0 """

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
