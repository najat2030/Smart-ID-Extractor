import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# إعداد Gemini
genai.configure(api_key="ضعي_مفتاحك_هنا")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Smart ID Batch Processor (Lightweight) 🚀")

uploaded_file = st.file_uploader("ارفعي ملف PDF للبطاقات", type=['pdf'])

if uploaded_file and st.button("استخراج البيانات"):
    with st.spinner("جاري المعالجة على سحابة جوجل..."):
        # رفع الملف مباشرة كـ Uploaded File لـ Gemini
        sample_file = genai.upload_file(uploaded_file, mime_type="application/pdf")
        
        prompt = """
        استخرجي من كل بطاقة في ملف الـ PDF التالي: الاسم، الرقم القومي، العنوان.
        أعيدي النتيجة بتنسيق JSON فقط: 
        [{"الاسم": "...", "الرقم_القومي": "...", "العنوان": "..."}]
        """
        
        response = model.generate_content([prompt, sample_file])
        
        # استخراج البيانات
        results = json.loads(response.text.replace("```json", "").replace("```", ""))
        
        df = pd.DataFrame(results)
        st.table(df)
        
        # تصدير إكسيل
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False)
        st.download_button("تحميل الملف ⬇️", towrite.getvalue(), "data.xlsx")
