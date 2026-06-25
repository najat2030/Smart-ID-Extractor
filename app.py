import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
import io
import time
import re

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
            # ✅ تصحيح 1: رفع الملف والانتظار حتى يصبح جاهزاً
            sample_file = genai.upload_file(uploaded_file, mime_type="application/pdf")
            
            # انتظار حتى يصبح الملف جاهزاً للمعالجة
            while sample_file.state.name == "PROCESSING":
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)
            
            if sample_file.state.name == "FAILED":
                st.error("❌ فشل في معالجة الملف على سيرفر Google. يرجى المحاولة مرة أخرى.")
                st.stop()
            
            # ✅ تصحيح 2: استخدام نموذج أحدث وأكثر دقة
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # ✅ تصحيح 3: تحسين الـ prompt لاستخراج CSV نظيف
            prompt = """
            أنت خبير في استخراج البيانات من بطاقات الرقم القومي المصرية.
            قم بتحليل ملف الـ PDF بدقة واستخرج بيانات كل بطاقة موجودة.
            
            أريد النتيجة فقط كـ CSV (مفصول بفاصلة ,) بدون أي مقدمات أو كلام جانبي.
            لا تضيف علامات ```csv أو ``` في البداية أو النهاية.
            
            الأعمدة يجب أن تكون:
            الاسم الكامل,الرقم القومي,العنوان,الوظيفة,الديانة,الحالة الاجتماعية,تاريخ الميلاد
            
            إذا لم تتوفر بعض البيانات في البطاقة، اترك الخانة فارغة.
            ابدأ مباشرة بالسطر الأول من البيانات (بدون عنوان الأعمدة).
            """
            
            # إرسال الملف والأمر للنموذج
            response = model.generate_content([sample_file, prompt])
            
            st.success("✨ تم استخراج البيانات بنجاح!")
            
            # ✅ تصحيح 4: تنظيف النص المستخرج من أي علامات كود
            csv_data = response.text.strip()
            
            # إزالة علامات ```csv و ``` لو موجودة
            csv_data = re.sub(r'^```(?:csv)?\s*', '', csv_data, flags=re.MULTILINE)
            csv_data = re.sub(r'\s*```$', '', csv_data, flags=re.MULTILINE)
            csv_data = csv_data.strip()
            
            # ✅ تصحيح 5: إضافة عنوان الأعمدة إذا لم يكن موجوداً
            columns = "الاسم الكامل,الرقم القومي,العنوان,الوظيفة,الديانة,الحالة الاجتماعية,تاريخ الميلاد"
            if columns not in csv_data and not csv_data.startswith(columns):
                csv_data = columns + "\n" + csv_data
            
            # ✅ تصحيح 6: معالجة الـ CSV مع تحديد الـ encoding
            try:
                df = pd.read_csv(io.StringIO(csv_data), encoding='utf-8')
                
                # ✅ تصحيح 7: التحقق من صحة البيانات
                if df.empty:
                    st.warning("⚠️ لم يتم استخراج أي بيانات من الملف.")
                    st.stop()
                
                # عرض عدد البطاقات المستخرجة
                st.write(f"📊 تم استخراج **{len(df)}** بطاقة بنجاح")
                
                # عرض الجدول بشكل تفاعلي وجميل على الشاشة
                st.dataframe(df, use_container_width=True)
                
                # ✅ تصحيح 8: تحويل الجدول إلى ملف إكسيل مع تحديد الـ engine
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
                
            except pd.errors.EmptyDataError:
                st.warning("⚠️ لم يتم استخراج بيانات صالحة. النص المستخرج:")
                st.code(csv_data)
                
            except pd.errors.ParserError as parse_err:
                st.warning(f"⚠️ مشكلة في تنسيق CSV. النص المستخرج:")
                st.code(csv_data)
                st.error(f"تفاصيل الخطأ: {str(parse_err)}")
                
            except Exception as csv_err:
                st.warning("⚠️ تم استخراج النص ولكن واجهنا مشكلة في التنسيق التلقائي للإكسيل. يمكنك رؤية النص بالأسفل:")
                st.code(csv_data)
                st.error(f"تفاصيل الخطأ: {str(csv_err)}")
            
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")
            st.info("💡 تأكد من:")
            st.markdown("""
            - أن مفتاح GEMINI_API_KEY صحيح ومفعّل
            - أن ملف PDF يحتوي على بطاقات واضحة
            - أن حجم الملف لا يتجاوز الحد المسموح
            """)
