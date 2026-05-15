import streamlit as st
import time

st.set_page_config(page_title="Belajar Bahasa Mandarin & Belanja | å­¦ä¸­æ–‡ä¸Žè´­ç‰©", page_icon="ðŸ‡¨ðŸ‡³", layout="wide")

# Mock data for e-commerce products
PRODUCTS = {
    "makanan": [
        {"name": "Latiao (è¾£æ¡)", "price": "Rp 15.000", "desc": "Cemilan pedas khas Tiongkok. | ä¸­å›½ç‰¹è‰²è¾£å‘³å°åƒã€‚"},
        {"name": "Boba Milk Tea DIY Kit (çç å¥¶èŒ¶åŒ…)", "price": "Rp 45.000", "desc": "Buat boba mu sendiri! | è‡ªå·±åŠ¨æ‰‹åšçç å¥¶èŒ¶ï¼"}
    ],
    "belajar": [
        {"name": "Buku HSK 1 (HSK 1 è¯æ±‡ä¹¦)", "price": "Rp 85.000", "desc": "Buku wajib untuk pemula. | åˆå­¦è€…å¿…å¤‡è¯æ±‡ä¹¦ã€‚"},
        {"name": "Kamus Bergambar (å›¾è§£è¯å…¸)", "price": "Rp 120.000", "desc": "Belajar kosakata dengan mudah. | è½»æ¾çœ‹å›¾å­¦è¯æ±‡ã€‚"}
    ]
}

def get_product_recommendation(user_input):
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in ["makan", "lapar", "makanan", "chi", "åƒ", "food", "enak"]):
        return PRODUCTS["makanan"]
    elif any(keyword in user_input_lower for keyword in ["belajar", "buku", "hsk", "xue", "å­¦", "study", "baca"]):
        return PRODUCTS["belajar"]
    return []

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Mari berlatih bahasa Mandarin. Apa yang ingin kamu bicarakan hari ini? | ä½ å¥½ï¼è®©æˆ‘ä»¬ç»ƒä¹ ä¸­æ–‡ã€‚ä½ ä»Šå¤©æƒ³èŠäº›ä»€ä¹ˆï¼Ÿ"}
    ]

if "recommended_products" not in st.session_state:
    st.session_state.recommended_products = []

# UI Layout
st.title("ðŸ—£ï¸ Latihan Mandarin & Rekomendasi | ä¸­æ–‡ç»ƒä¹ ä¸ŽæŽ¨è")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("ðŸ’¬ Chat Box | èŠå¤©æ¡†")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ketik pesanmu di sini | åœ¨è¿™é‡Œè¾“å…¥ä½ çš„ä¿¡æ¯..."):
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
                
                # Menggunakan API Key yang diberikan
                api_key = "AIzaSyCqPSVF56c-rVdkiXWqy6FOAxHxLqyHn98"
                genai.configure(api_key=api_key)
                
                system_prompt = "Kamu adalah guru bahasa Mandarin. Balas menggunakan bahasa Indonesia dan Mandarin (dengan Pinyin). Jawablah dengan singkat, ramah, dan natural."
                model = genai.GenerativeModel("gemini-1.5-flash-latest", system_instruction=system_prompt)
                
                # Format messages for Gemini
                gemini_messages = []
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
    st.subheader("ðŸ›ï¸ Rekomendasi Produk | æŽ¨èäº§å“")
    st.markdown("Produk yang mungkin kamu suka | æ ¹æ®å¯¹è¯ä¸ºä½ æŽ¨èçš„å•†å“ï¼š")
    
    if st.session_state.recommended_products:
        for prod in st.session_state.recommended_products:
            with st.container():
                st.markdown(f"**{prod['name']}**")
                st.markdown(f"ðŸ·ï¸ *{prod['price']}*")
                st.caption(prod['desc'])
                st.button(f"Beli | è´­ä¹°", key=prod['name'])
                st.markdown("---")
    else:
        st.info("Mulai obrolan tentang makanan (makan) atau belajar (buku/HSK) untuk melihat rekomendasi! | å°è¯•èŠèŠé£Ÿç‰©(åƒ)æˆ–å­¦ä¹ (ä¹¦)æ¥çœ‹çœ‹äº§å“æŽ¨èå§ï¼")



