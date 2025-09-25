# 🎭 もしもAI - Streamlit × LLM エンタメチャットアプリ

「もしも猫が話せたら？」「もしも織田信長が令和にいたら？」  
そんな“妄想”をLLMで現実にする、キャラクター選択型の対話アプリです。

---

## 🚀 概要

このアプリは、OpenAI API と Streamlit を使って構築した  
**対話型ジェネレーティブAIアプリ**です。  
ユーザーはキャラクターを選び、自然な会話を楽しむことができます。

| 🐱 猫 | ⚔️ 織田信長 | 🚀 宇宙船AI |
|------|-----------|------------|
| ツンデレで知的な猫が皮肉を交えて回答 | 戦国時代の思考で現代を語る信長 | 論理的な宇宙船AIが冷静に応答 |

---

## 🧰 使用技術

- 🧠 **LLM API**: OpenAI GPT-4 / GPT-4o-mini  
- 💻 **フレームワーク**: [Streamlit](https://streamlit.io/)  
- 📁 **構成管理**: Git + GitHub  
- ⚙️ **その他ライブラリ**: `python-dotenv`, `PyYAML`

---

## 🗂️ プロジェクト構成
```
moshimo-ai/
├─ app.py                # メインアプリ本体
├─ characters.yaml      # キャラクター設定（人格プロンプト）
├─ requirements.txt     # 依存パッケージ
├─ .env.example         # 環境変数テンプレート
└─ assets/              # 各キャラクターのアイコン画像
   ├─ cat.png
   ├─ oda.png
   └─ spaceship.png
```
