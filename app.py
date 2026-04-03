import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# --- تفعيل المحرك (مفتاحك الشخصي) ---
API_KEY = "AIzaSyCBaq0_Fq3F2SEkEs1SC_n6fpIGQYP8XwQ"

# محاولة الاتصال بالذكاء الاصطناعي
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro') # تم تغيير الموديل لنسخة أكثر استقراراً
except Exception as e:
    st.error(f"فشل في إعداد المحرك: {e}")

# --- دالة الصياغة ---
def ask_ai(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"الذكاء الاصطناعي بيقولك: {e}"

# --- الواجهة ---
st.set_page_config(page_title="الهيئة القومية للتأمين الاجتماعي", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("⚖️ الإدارة القانونية - البحيرة")
    code = st.text_input("أدخل كود الدخول (WALID2026)", type="password")
    if st.button("دخول"):
        if code == "WALID2026":
            st.session_state.auth = True
            st.rerun()
else:
    st.sidebar.title("📁 الأقسام")
    choice = st.sidebar.radio("اختر القسم", ["القضايا", "المكتبة"])

    if choice == "القضايا":
        st.header("📝 صياغة مذكرات الدفاع")
        case_data = st.text_area("انسخ هنا وقائع الدعوى أو العريضة:")
        
        if st.button("🚀 ابدأ الصياغة الذكية"):
            if case_data:
                with st.spinner("جاري التواصل مع محرك الذكاء الاصطناعي..."):
                    # أمر الصياغة المحدد
                    full_prompt = f"""
                    أنت مستشار قانوني للهيئة القومية للتأمين الاجتماعي بمصر.
                    قم بصياغة مذكرة دفاع بناءً على هذه الوقائع: {case_data}
                    يجب أن تشمل:
                    1- ترتيب الدفوع قانونياً.
                    2- المادة القانونية من قانون 148 لسنة 2019 ثم شرحها ثم النتيجة.
                    3- خانات التوقيع (عضو الإدارة / مدير الإدارة).
                    """
                    result = ask_ai(full_prompt)
                    st.markdown("### المذكرة المقترحة:")
                    st.write(result)
            else:
                st.warning("برجاء إدخال بيانات القضية أولاً")

    elif choice == "المكتبة":
        st.write("📚 قسم المكتبة القانونية جاهز لرفع الملفات.")
