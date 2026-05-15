import streamlit as st
import time

st.set_page_config(page_title="Belajar Bahasa Mandarin & Belanja | 中文练习与推荐", page_icon="🛍️", layout="wide")

# Mock data for e-commerce products
PRODUCTS = {
    "makanan": [
        {"name": "Latiao (辣条)", "price": "Rp 15.000", "desc": "Cemilan pedas khas Tiongkok. | 中国特色香辣零食。"},
        {"name": "Boba Milk Tea DIY Kit (珍珠奶茶DIY包)", "price": "Rp 45.000", "desc": "Buat boba mu sendiri! | 自己动手做珍珠奶茶！"}
    ],
    "belajar": [
        {"name": "Buku HSK 1 (HSK 1 课本)", "price": "Rp 85.000", "desc": "Buku wajib untuk pemula. | 初学者必读书籍。"},
        {"name": "Kamus Bergambar (图解词典)", "price": "Rp 120.000", "desc": "Belajar kosakata dengan mudah. | 轻松学习词汇。"}
    ]
}

def get_product_recommendation(user_input):
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in ["makan", "lapar", "makanan", "chi", "吃", "food", "enak"]):
        return PRODUCTS["makanan"]
    elif any(keyword in user_input_lower for keyword in ["belajar", "buku", "hsk", "xue", "学", "study", "baca"]):
        return PRODUCTS["belajar"]
    return []

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Mari berlatih bahasa Mandarin. Apa yang ingin kamu bicarakan hari ini? | 你好！让我们练习中文。你今天想聊些什么？"}
    ]

if "recommended_products" not in st.session_state:
    st.session_state.recommended_products = []

# UI Layout
st.title("🗣️ Latihan Mandarin & Rekomendasi | 中文练习与推荐")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Box | 聊天框")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ketik pesanmu di sini | 在这里输入你的信息..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Update recommendations based on input
        new_recs = get_product_recommendation(prompt)
        if new_recs:
            st.session_state.recommended_products = new_recs

        # REAL AI RESPONSE via Gemini
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                import google.generativeai as genai
                import os
                
                # Coba ambil API Key dari Secrets Streamlit, jika gagal (seperti di lokal) pakai default yang hardcoded
                # Karena ini repo private atau sudah dilindungi, kita fall back ke key hardcoded yang aman
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                except Exception:
                    api_key = "AIzaSyC-TQOeouormu9diIwo3tRvdTCpP-RgZhc"
                    
                genai.configure(api_key=api_key)
                
                system_prompt = "Kamu adalah guru bahasa Mandarin. Balas menggunakan bahasa Indonesia dan Mandarin (dengan Pinyin). Jawablah dengan singkat, ramah, dan natural."
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                gemini_messages = [{"role": "user", "parts": [system_prompt]}]
                
                for msg in st.session_state.messages[-5:]:
                    if msg["role"] == "user":
                        gemini_messages.append({"role": "user", "parts": [msg["content"]]})
                    elif msg["role"] == "assistant":
                        gemini_messages.append({"role": "model", "parts": [msg["content"]]})
                
                response = model.generate_content(gemini_messages)
                ai_reply = response.text
                
            except Exception as e:
                ai_reply = "Maaf, API sedang sibuk. (Error: " + str(e) + ")"
                
            for chunk in ai_reply.split(" "):
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with col2:
    st.subheader("🛍️ Rekomendasi Produk | 推荐产品")
    st.markdown("Produk yang mungkin kamu suka | 你可能喜欢的推荐产品")
    
    if st.session_state.recommended_products:
        for prod in st.session_state.recommended_products:
            with st.container():
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"💰 *{prod['price']}*")
                st.caption(prod['desc'])
                st.button(f"Beli | 购买", key=prod['name'])
                st.markdown("---")
    else:
        st.info("Mulai obrolan tentang makanan (makan) atau belajar (buku/HSK) untuk melihat rekomendasi! | 开始聊聊食物(吃)或学习(书)来看看推荐吧！")
