import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="DZ-Ad Pro", layout="centered")

# الربط الآمن مع Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🚀 DZ-Ad Pro")
    st.write("اكتب إعلاناتك بالدارجة الجزائرية باستخدام الذكاء الاصطناعي")

    user_email = st.text_input("الإيميل:")
    if user_email:
        img_file = st.file_uploader("ارفع صورة المنتج", type=["jpg", "png", "jpeg"])
        info = st.text_input("تفاصيل (السعر، المكان...):")
        
        if st.button("توليد الإعلان ✨"):
            with st.spinner("جاري العمل..."):
                prompt = f"اكتب إعلانين جذابين بالدارجة الجزائرية لهذا المنتج. الإضافات: {info}"
                if img_file:
                    img = Image.open(img_file)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                st.markdown("---")
                st.write(response.text)
                st.balloons()
else:
    st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets")
