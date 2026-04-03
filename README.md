import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# --- 1. إعداد المحرك الذكي (Gemini) بمفتاحك ---
API_KEY = "AIzaSyCBaq0_Fq3F2SEkEs1SC_n6fpIGQYP8XwQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. دالة الصياغة القانونية الاحترافية (المادة -> الشرح -> النتيجة) ---
def legal_ai_drafter(data_input, category):
    prompt = f"""
    بصفتك المستشار القانوني للهيئة القومية للتأمين الاجتماعي (منطقة البحيرة).
    المطلوب: صياغة {category} احترافية بناءً على: {data_input}
    
    القواعد الإلزامية:
    1. ابدأ بـ "باسم الشعب" ثم "الهيئة القومية للتأمين الاجتماعي - الإدارة القانونية".
    2. ترتيب الدفوع قانونياً (شكلي ثم موضوعي).
    3. الهيكل لكل دفع: (عنوان الدفع -> نص المادة من قانون 148 لسنة 2019 -> الشرح القانوني -> النتيجة).
    4. الصياغة من وجهة نظر الهيئة حصراً.
    5. في النهاية: 
       عن الهيئة / ....................
       عضو الإدارة القانونية / .................... (توقيع)
       مدير الإدارة القانونية / .................... (توقيع)
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "برجاء التأكد من اتصال الإنترنت وصلاحية الـ API Key."

# --- 3. إعدادات واجهة البرنامج ---
st.set_page_config(page_title="الإدارة القانونية - التأمين الاجتماعي", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    st.title("🏛️ الإدارة القانونية بالهيئة القومية للتأمين الاجتماعي")
    st.info("مع تحيات أ/ وليد حماد - الإدارة العامة للشئون القانونية - البحيرة")
    code = st.text_input("أدخل كود الدخول الخاص بك", type="password")
    if st.button("دخول"):
        if code == "WALID2026": # كود الدخول الخاص بك
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الكود غير صحيح!")
else:
    # --- 4. نظام الشجرة (Sidebar) ---
    st.sidebar.title("📁 أقسام الإدارة")
    menu = st.sidebar.radio("القائمة الرئيسية", [
        "1. الإدارة العامة للقضايا",
        "2. الإدارة العامة للفتوى",
        "3. التحقيقات والنيابات",
        "4. المكتبة القانونية"
    ])

    # --- القسم الأول: القضايا ---
    if menu == "1. الإدارة العامة للقضايا":
        st.header("⚖️ إدارة القضايا والطعون")
        court_lvl = st.selectbox("المحكمة", ["الابتدائية", "الاستئنافية", "النقض", "مجلس الدولة", "الإدارية العليا"])
        doc_type = st.selectbox("نوع السند", ["مذكرة دفاع (الهيئة مدعى عليها)", "مذكرة دفاع (الهيئة مدعية)", "صحيفة طعن"])
        
        col1, col2 = st.columns(2)
        with col1:
            c_name = st.text_input("المحكمة / الدائرة")
            c_no = st.text_input("رقم الدعوى / السنة")
        with col2:
            parties = st.text_input("أسماء الخصوم وصفاتهم")
        
        facts = st.text_area("ملخص الوقائع (أو انسخ نص العريضة هنا)")
        
        if st.button("🚀 صياغة ذكية"):
            with st.spinner("جاري الصياغة وترتيب الدفوع..."):
                input_data = f"المحكمة: {c_name}, رقم: {c_no}, الخصوم: {parties}, الوقائع: {facts}"
                draft = legal_ai_drafter(input_data, doc_type)
                st.markdown("---")
                st.subheader("المسودة النهائية:")
                st.write(draft)
                
                # تحميل Word
                doc = Document()
                doc.add_paragraph(draft)
                bio = BytesIO()
                doc.save(bio)
                st.download_button("💾 تحميل ملف Word", bio.getvalue(), "Legal_Draft.docx")

    # --- القسم الثاني: الفتوى ---
    elif menu == "2. الإدارة العامة للفتوى":
        st.header("📜 قسم الإفتاء القانوني")
        f_cat = st.selectbox("النوع", ["فتاوى عامة", "إصابات عمل", "زواج عرفي"])
        f_data = st.text_area("عرض الوقائع ومثار البحث")
        if st.button("صياغة الرأي"):
            res = legal_ai_drafter(f_data, f"مذكرة رأي قانوني - {f_cat}")
            st.write(res)

    # --- القسم الثالث: التحقيقات ---
    elif menu == "3. التحقيقات والنيابات":
        st.header("🔍 سجل التحقيقات")
        t_type = st.selectbox("الجهة", ["تحقيقات الهيئة", "النيابة الإدارية", "النيابة العامة"])
        t_info = st.text_input("رقم التحقيق / اسم المخالف")
        t_facts = st.text_area("ملخص المخالفة")
        if st.button("صياغة مذكرة التصرف"):
            res = legal_ai_drafter(t_facts, f"مذكرة تصرف في تحقيق - {t_type}")
            st.write(res)

    # --- القسم الرابع: المكتبة ---
    elif menu == "4. المكتبة القانونية":
        st.header("📚 المكتبة الرقمية")
        lib_cat = st.selectbox("التصنيف", ["قوانين", "لوائح", "كتب
