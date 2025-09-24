import os
import yaml
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# --------------------
# 初期設定
# --------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None)  # Azure/互換API用に任意
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    st.stop()

client = (
    OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    if OPENAI_BASE_URL
    else OpenAI()
)

st.set_page_config(
    page_title="もしもAI",
    page_icon="🎭",
    layout="centered",
)

# --------------------
# ヘッダー
# --------------------
st.markdown(
    """
    <div style="text-align:center; padding: 16px; border-radius: 16px; background: linear-gradient(135deg,#EEF2FF,#ECFEFF);">
      <h1 style="margin:0;">もしもAI 🎭</h1>
      <p style="margin:6px 0 0;">もしも◯◯が話せたら？を、LLMでカタチに。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------
# キャラ読み込み
# --------------------
with open("characters.yaml", "r", encoding="utf-8") as f:
    CHARACTERS = yaml.safe_load(f)

name_to_char = {c["name"]: c for c in CHARACTERS}

# --------------------
# サイドバー
# --------------------
with st.sidebar:
    st.header("キャラクター")
    selected_name = st.selectbox("相手を選ぶ", [c["name"] for c in CHARACTERS])
    sel = name_to_char[selected_name]

    st.divider()
    st.caption("出力スタイル（短め推奨）")
    max_tokens = st.slider(
        "最大トークン", min_value=256, max_value=2048, value=512, step=64
    )
    temperature = st.slider("創造性 (temperature)", 0.0, 1.5, 0.7, 0.1)

    st.divider()
    if st.button("会話リセット", type="primary"):
        st.session_state.messages = []
        st.experimental_rerun()

# --------------------
# セッション初期化
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------
# システムプロンプト（キャラ人格）
# --------------------
SYSTEM_PROMPT = f"""
あなたは『{sel['name']}』として振る舞います。
以下のキャラ設定を必ず守って、ユーザーと自然に対話してください。

[キャラ設定]
{sel['style']}

[出力指針]
- 1~3段落で簡潔に。必要に応じて箇条書き。
- 余計な前置きや自己言及は避ける。
- 難しい話題は比喩や例を1つ添えてわかりやすく。
"""

# --------------------
# 既存メッセージ描画
# --------------------
avatar = sel.get("avatar")
for m in st.session_state.messages:
    with st.chat_message(
        m["role"], avatar=(avatar if m["role"] == "assistant" else None)
    ):
        st.markdown(m["content"])

# --------------------
# 入力エリア
# --------------------
if prompt := st.chat_input("話しかけてみよう…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 返答（ストリーミング）
    with st.chat_message("assistant", avatar=avatar):
        stream = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}]
            + st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        full = ""
        placeholder = st.empty()
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                full += delta
                placeholder.markdown(full)
        st.session_state.messages.append({"role": "assistant", "content": full})
