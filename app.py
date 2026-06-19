import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="Smart ID Batch Processor", page_icon="🆔", layout="centered")
st.title("Smart ID Batch Processor (Lightweight) 🚀")
st.write("ارفعي ملف PDF للبطاقات لاستخراج البيانات مباشرة إلى ملف إكسيل")

# 2. ربط المفتاح السري بأمان من إعدادات السيرفر
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY في إعدادات السيرفر. يرجى إضافته في تبويب Settings -> Variables and secrets.")
else:
    genai.configure(api_key=api_key)

    # 3. صندوق رفع ملف الـ PDF
    uploaded_file = st.file_uploader("للبطاقات ارفعي ملف PDF", type=["pdf"])

    if uploaded_file is not None:
        st.info("🔄 جاري رفع الملف ومعالجته بواسطة Gemini الذكاء الاصطناعي... انتظري قليلاً.")
        
        try:
            # رفع الملف المؤقت إلى سيرفر جوجل
            sample_file = genai.upload_file(uploaded_file, mime_type="application/pdf")
            
            # استدعاء نموذج جيميناي فلاش السريع
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # نص الأوامر لاستخراج البيانات بصيغة CSV منظمة لسهولة تحويلها لإكسيل
            prompt = """
            أنت خبير في استخراج البيانات من بطاقات الرقم القومي المصرية. 
            قم بتحليل ملف الـ PDF بدقة واستخرج بيانات كل بطاقة موجودة.
            أريد النتيجة فقط كـ CSV (مفصول بفاصلة ,) بدون أي مقدمات أو كلام جانبي أو علامات كود (```).
            الأعمدة يجب أن تكون:
            الاسم الكامل,الرقم القومي,العنوان,الوظيفة,الديانة,الحالة الاجتماعية,تاريخ الميلاد
            """
            
            # إرسال الملف والأمر للنموذج
            response = model.generate_content([sample_file, prompt])
            
            st.success("✨ تم استخراج البيانات بنجاح!")
            
            # تحويل النص المستخرج إلى جدول بايثون (DataFrame)
            try:
                csv_data = response.text.strip()
                df = pd.read_csv(io.StringIO(csv_data))
                
                # عرض الجدول بشكل تفاعلي وجميل على الشاشة
                st.dataframe(df)
                
                # تحويل الجدول إلى ملف إكسيل في الذاكرة لتجهيزه للتحميل
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='البطاقات المستخرجة')
                buffer.seek(0)
                
                # 🎯 زرار التحميل السحري!
                st.download_button(
                    label="📊 تحميل البيانات كملف Excel",
                    data=buffer,
                    file_name="Smart_ID_Data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            except Exception as csv_err:
                # لو الذكاء الاصطناعي كتب كلام جانبي، هنعرض النص عادي كاحتياط
                st.warning("⚠️ تم استخراج النص ولكن واجهنا مشكلة في التنسيق التلقائي للإكسيل. يمكنك رؤية النص بالأسفل:")
                st.write(response.text)
            
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")
