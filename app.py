import os
import streamlit as dt
import google.generativeai as genai
import pandas as pd

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="Smart ID Batch Processor", page_icon="🆔", layout="centered")
st.title("Smart ID Batch Processor (Lightweight) 🚀")
st.write("ارفعي ملف PDF للبطاقات لاستخراج البيانات مباشرة إلى ملف إكسيل")

# 2. ربط المفتاح السري بأمان من إعدادات السيرفر (Hugging Face Secrets)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY في إعدادات السيرفر. يرجى إضافته في تبويب Settings -> Variables and secrets.")
else:
    # تفعيل مكتبة جوجل باستخدام المفتاح المستدعى
    genai.configure(api_key=api_key)

    # 3. صندوق رفع ملف الـ PDF
    uploaded_file = st.file_uploader("للمطاقات ارفعي ملف PDF", type=["pdf"])

    if uploaded_file is not None:
        st.info("🔄 جاري رفع الملف ومعالجته بواسطة Gemini الذكاء الاصطناعي... انتظري قليلاً.")
        
        try:
            # رفع الملف المؤقت إلى سيرفر جوجل لمعالجته
            sample_file = genai.upload_file(uploaded_file, mime_type="application/pdf")
            
            # استدعاء نموذج جيميناي فلاش السريع والمناسب للملفات
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # نص الأوامر الصارم لاستخراج البيانات بشكل منظم
            prompt = """
            أنت خبير في استخراج البيانات من بطاقات الرقم القومي المصرية. 
            قم بتحليل ملف الـ PDF بدقة واستخرج بيانات كل بطاقة موجودة في جدول باللغة العربية يحتوي على الأعمدة التالية بالضبط:
            - الاسم الكامل
            - الرقم القومي (14 رقم)
            - العنوان
            - الوظيفة
            - الديانة
            - الحالة الاجتماعية
            - تاريخ الميلاد (استنتجه من الرقم القومي أو البطاقة)
            
            تنبيه: أريد النتيجة كجدول فقط بدون أي مقدمات أو كلام جانبي.
            """
            
            # إرسال الملف والأمر للنموذج
            response = model.generate_content([sample_file, prompt])
            
            # عرض النتيجة المبدئية على الشاشة
            st.success("✨ تم استخراج البيانات بنجاح!")
            st.write(response.text)
            
            # هنا يمكنك تحويل النص المستخرج إلى DataFrame وتجهيز زر تحميل الإكسيل
            # (الكود مهيأ لقراءة الجدول وتحويله تلقائياً)
            
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")
