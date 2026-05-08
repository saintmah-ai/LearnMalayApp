import streamlit as st
import time

st.set_page_config(page_title="Belajar Bahasa Mandarin & Belanja | 学习与购物", page_icon="🛒", layout="wide")

PRODUCTS = {
    "makanan": [
        {"name": "Latiao (辣条)", "price": "Rp 15.000", "desc": "Cemilan pedas khas Tiongkok. | 中国特色辣味零食。"},
        {"name": "Boba Milk Tea DIY Kit (珍珠奶茶DIY套装)", "price": "Rp 45.000", "desc": "Buat boba mu sendiri! | 自己制作珍珠奶茶！"}
    ],
    "belajar": [
        {"name": "Buku HSK 1 (HSK 1 教程)", "price": "Rp 85.000", "desc": "Buku wajib untuk pemula. | 初学者必读教程。"},
        {"name": "Kamus Bergambar (看图词典)", "price": "Rp 120.000", "desc": "Belajar kosakata dengan mudah. | 轻松学习词汇。"}
    ]
}

def get_product_recommendation(user_input):
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in ["makan", "lapar", "makanan", "chi", "吃", "food", "enak"]):
        return PRODUCTS["makanan"]
    elif any(keyword in user_input_lower for keyword in ["belajar", "buku", "hsk", "xue", "学", "study", "baca"]):
        return PRODUCTS["belajar"]
    return []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Mari berlatih bahasa Mandarin. Apa yang ingin kamu bicarakan hari ini? | 你好！让我们练习中文。你今天想聊些什么？"}
    ]

if "recommended_products" not in st.session_state:
    st.session_state.recommended_products = []

st.title("🗣️ Latihan Mandarin & Rekomendasi | 中文练习与推荐")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Box | 聊天框")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ketik pesanmu di sini | 在这里输入你的信息..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        new_recs = get_product_recommendation(prompt)
        if new_recs:
            st.session_state.recommended_products = new_recs

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                import g4f.client
                client = g4f.client.Client()
                
                system_prompt = "Kamu adalah guru bahasa Mandarin. Balas menggunakan bahasa Indonesia dan Mandarin (dengan Pinyin). Jawablah dengan singkat, ramah, dan natural."
                
                api_messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages[-5:]:
                    if msg["role"] != "system":
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages
                )
                
                ai_reply = response.choices[0].message.content
                ai_reply = ai_reply.split("Need proxies cheaper")[0].strip()
                ai_reply = ai_reply.split("https://op.wtf")[0].strip()
                
            except Exception as e:
                ai_reply = "Maaf, API sedang sibuk. (Error: " + str(e) + ")"
                
            for chunk in ai_reply.split(" "):
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with col2:
    st.subheader("🛍️ Rekomendasi Produk | 推荐产品")
    st.markdown("Produk yang mungkin kamu suka | 你可能喜欢的推荐产品")
    
    if st.session_state.recommended_products:
        for prod in st.session_state.recommended_products:
            with st.container():
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"🏷️ *{prod['price']}*")
                st.caption(prod['desc'])
                st.button(f"Beli | 购买", key=prod['name'])
                st.markdown("---")
    else:
        st.info("Mulai obrolan tentang makanan (makan) atau belajar (buku/HSK) untuk melihat rekomendasi! | 开始聊聊食物(吃)或学习(书)来看看推荐吧！")
