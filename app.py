import os
import yaml
import random
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# --------------------
# ページ設定（最初に設定する必要がある）
# --------------------
st.set_page_config(
    page_title="もしもAI",
    page_icon="🎭",
    layout="centered",
)

# --------------------
# 初期設定
# --------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None)  # Azure/互換API用に任意
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    st.error("🚨 OpenAI APIキーが設定されていません！")
    st.info("💡 .envファイルにOPENAI_API_KEYを設定してください")
    st.stop()

client = (
    OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    if OPENAI_BASE_URL
    else OpenAI(api_key=OPENAI_API_KEY)
)

# --------------------
# ヘッダー
# --------------------
st.markdown(
    """
    <div style="text-align:center; padding: 24px; border-radius: 20px; 
                background: #F5F5F5;  /* 単色の淡いグレー */
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                border: 1px solid #D3D3D3;">
      <h1 style="margin:0; color: #333333; text-shadow: none; font-size: 2em;">
        もしもAI 🎭✨
      </h1>
      <p style="margin: 12px 0 0; color: #666666; font-size: 1em; font-weight: 500;">
        もしも◯◯が話せたら？を、LLMでカタチに。
      </p>
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
    # キャラクター選択セクション
    st.markdown(
        """
        <div style="background: #F8F8F8;  /* 単色の淡いグレー */
                    padding: 15px; border-radius: 15px; margin-bottom: 20px;
                    border: 1px solid #D3D3D3;">
            <h2 style="color: #333333; text-align: center; margin: 0; font-size: 1.5em;">
                🎭 キャラクター選択 ✨
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_name = st.selectbox("🎪 相手を選ぶ", [c["name"] for c in CHARACTERS])
    sel = name_to_char[selected_name]

    # 設定セクション
    st.markdown("---")
    st.markdown(
        """
        <div style="background: #F8F8F8;  /* 単色の淡いグレー */
                    padding: 15px; border-radius: 15px; margin: 15px 0;
                    border: 1px solid #D3D3D3;">
            <h3 style="color: #333333; text-align: center; margin: 0; font-size: 1.2em;">
                ⚙️ 出力スタイル設定 🎨
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    max_tokens = st.slider(
        "📝 最大トークン", min_value=256, max_value=2048, value=512, step=64
    )
    temperature = st.slider("🎨 創造性 (temperature)", 0.0, 1.5, 0.7, 0.1)

    st.markdown("---")

    # 現在の会話数を表示
    if st.session_state.get("messages"):
        msg_count = len(st.session_state.messages)
        st.caption(f"💬 会話数: {msg_count // 2}回")

    # リセットボタンを特別にスタイリング
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 会話リセット", type="primary"):
            st.session_state.messages = []
            st.rerun()

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

# メッセージがない場合の初期表示
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align: center; padding: 40px; 
                    background: linear-gradient(135deg, #FFF8DC, #FFE4E1, #E0FFFF);
                    border-radius: 20px; margin: 20px 0;
                    border: 2px dashed #FFB6C1;">
            <h3 style="color: #FF6347; margin-bottom: 20px;">
                🎭 {} との会話を始めよう！ ✨
            </h3>
            <p style="color: #4682B4; font-size: 1.1em;">
                下のチャット欄から気軽に話しかけてください 🌈
            </p>
        </div>
        """.format(
            sel["name"]
        ),
        unsafe_allow_html=True,
    )

for m in st.session_state.messages:
    with st.chat_message(
        m["role"], avatar=(avatar if m["role"] == "assistant" else None)
    ):
        st.markdown(m["content"])

# --------------------
# 入力エリア
# --------------------
if prompt := st.chat_input("話しかけてみよう..."):
    # ユーザーメッセージをセッションに追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 返答
    with st.chat_message("assistant", avatar=avatar):
        try:
            with st.spinner("考え中..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                    + st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
