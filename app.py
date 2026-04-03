import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات البرنامج ---
st.set_page_config(page_title="الإدارة القانونية - الهيئة القومية للتأمين الاجتماعي", layout="wide")

# --- نظام تسجيل الدخول والصلاحيات ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None # admin or member

def check_login(code):
    if code == "WALID-ADMIN-2026": # كود المدير (أ/ وليد)
        st.session_state.logged_in = True
        st.session_state.user_role = "admin"
    elif code == "MEMBER-NOSI-2026": # كود الأعضاء
        st.session_state.logged_in = True
        st.session_state.user_role = "member"
    else:
        st.error("كود الدخول غير صحيح!")

# --- واجهة الدخول ---
if not st.session_state.logged_in:
    st.title("⚖️ الهيئة القومية للتأمين الاجتماعي")
    st.subheader("الإدارة القانونية - ديوان عام منطقة البحيرة")
    code = st.text_input("أدخل كود الدخول الخاص بك", type="password")
    if st.button("دخول"):
        check_login(code)
else:
    # --- الهيكل الرئيسي (نظام الشجرة) ---
    st.sidebar.title("القائمة الرئيسية")
    st.sidebar.write(f"مرحباً: {st.session_state.user_role}")
    
    if st.session_state.user_role == "admin":
        main_menu = st.sidebar.radio("اختر القسم:", 
            ["الإدارة العامة للقضايا", "الإدارة العامة للفتوى", "التحقيقات والنيابات", "المكتية القانونية", "إدارة الأعضاء"])
    else:
        main_menu = st.sidebar.radio("اختر القسم:", ["المكتية القانونية"])

    # --- 1. قسم القضايا ---
    if main_menu == "الإدارة العامة للقضايا":
        st.header("⚖️ الإدارة العامة للقضايا (القسم القضائي)")
        sub_tab = st.selectbox("نوع المحكمة", ["القضاء العادي", "مجلس الدولة", "تسجيل الدعاوى/الطعون", "البحث في الأرشيف"])
        
        if sub_tab == "القضاء العادي":
            type_case = st.selectbox("الدرجة", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"])
            
            with st.expander("📝 صياغة مذكرة دفاع / صحيفة"):
                col1, col2 = st.columns(2)
                with col1:
                    court_name = st.text_input("المحكمة")
                    case_no = st.text_input("رقم الدعوى / السنة")
                with col2:
                    client_info = st.text_input("اسم المدعي وصفته")
                    def_info = st.text_input("اسم المدعى عليه وصفته")
                
                facts = st.text_area("ملخص الوقائع")
                uploaded_file = st.file_uploader("أو ارفع صورة الصحيفة لتحليلها بالذكاء الاصطناعي")
                
                if st.button("صياغة المذكرة قانونياً"):
                    st.info("جاري الصياغة طبقاً لدفوع الهيئة وترتيب المواد القانونية...")
                    # هنا يتم الربط مع API الذكاء الاصطناعي
                    st.markdown(f"""
                    ### مذكرة بدفاع الهيئة
                    **المحكمة:** {court_name} | **رقم الدعوى:** {case_no}
                    
                    **الدفاع:**
                    1. المادة القانونية: (يتم استخراجها من المكتبة)
                    2. الشرح والنتيجة...
                    
                    ---
                    **عن الهيئة**
                    عضو الإدارة القانونية: ....................
                    مدير الإدارة القانونية: ....................
                    """)

    # --- 2. المكتبة القانونية (متاحة للجميع) ---
    elif main_menu == "المكتية القانونية":
        st.header("📚 المكتبة القانونية الرقمية")
        lib_cat = st.selectbox("التصنيف", ["قوانين", "لوائح", "قرارات وزارية", "منشورات رئيس الهيئة", "فتاوى مجلس الدولة", "أحكام قضائية"])
        
        uploaded_lib = st.file_uploader(f"تحميل ملف جديد في قسم {lib_cat}")
        if uploaded_lib and st.session_state.user_role == "admin":
            st.success("تم الحفظ في قاعدة بيانات المكتبة")
        
        st.write("ملفات متاحة للتحميل:")
        st.button("تحميل قانون التأمينات الجديد.pdf")

    # --- 3. إدارة الأعضاء (لأستاذ وليد فقط) ---
    elif main_menu == "إدارة الأعضاء":
        st.subheader("⚙️ التحكم في الصلاحيات")
        st.write("الأعضاء النشطون حالياً: 5")
        if st.button("إلغاء كود العضو الحالي"):
            st.warning("تم حظر الكود")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
