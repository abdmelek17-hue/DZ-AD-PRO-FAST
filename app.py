import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعداد الصفحة
st.set_page_config(page_title="DZ-Ad Pro", page_icon="🚀")

# 2. جلب المفتاح السري من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح السري GEMINI_API_KEY غير موجود في Secrets!")

# 3. دالة سحرية لتصغير حجم الصورة (لحل مشكلة الثقل)
def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    # تصغير الصورة إذا كانت كبيرة جداً للحفاظ على سرعة التطبيق
    max_size = 800
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.LANCZOS)
    return image

# 4. واجهة المستخدم
st.title("🚀 DZ-Ad Pro")
st.subheader("اكتب إعلاناتك بالدارجة الجزائرية باستخدام الذكاء الاصطناعي")

email = st.text_input("الإيميل:")
uploaded_file = st.file_uploader("ارفع صورة المنتج هنا...", type=["jpg", "jpeg", "png"])
details = st.text_area("تفاصيل إضافية (السعر، المكان، المميزات...):")

if st.button("توليد الإعلان ✨"):
    if uploaded_file and email:
        with st.spinner("جاري التحليل... انتظر قليلاً"):
            try:
                # معالجة الصورة وتصغيرها
                img = process_image(uploaded_file)
                
                # إعداد النموذج
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # الأمر (Prompt)
                prompt = f"""
                أنت خبير تسويق جزائري. قم بتحليل هذه الصورة واكتب إعلاناً جذاباً ومؤثراً 
                باللهجة الجزائرية (الدارجة) بناءً على هذه التفاصيل: {details}.
                استخدم إيموجي مناسبة واجعل النص ممتعاً للزبون الجزائري.
                """
                
                # إرسال الطلب
                response = model.generate_content([prompt, img])
                
                st.success("تم توليد الإعلان بنجاح!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ بسيط: {e}")
                st.info("نصيحة: جرب رفع صورة أصغر أو أعد المحاولة بعد دقيقة.")
    else:
        st.warning("يرجى إدخال الإيميل ورفع صورة أولاً.")

# 5. لوحة التحكم البسيطة (للمهندس)
st.sidebar.markdown("---")
if st.sidebar.text_input("كلمة سر الإدارة", type="password") == "ENS_2026":
    st.sidebar.success("مرحباً بك يا مهندس!")
    st.sidebar.write("تطبيقك شغال بنظام Gemini 1.5 Flash")
