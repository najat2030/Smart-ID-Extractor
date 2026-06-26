<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>استخراج بيانات البطاقات - OCR مجاني</title>
    
    <!-- Tesseract.js للـ OCR -->
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
    
    <!-- PDF.js لقراءة ملفات PDF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
    
    <!-- SheetJS لتحويل البيانات لـ Excel -->
    <script src="https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 20px;
            text-align: center;
            margin: 30px 0;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        
        .upload-area:hover {
            background: #eef0ff;
            border-color: #764ba2;
        }
        
        .upload-area.dragover {
            background: #e0e3ff;
            border-color: #764ba2;
        }
        
        .upload-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 18px;
            color: #333;
            margin-bottom: 10px;
        }
        
        .upload-hint {
            font-size: 14px;
            color: #666;
        }
        
        #file-input {
            display: none;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 5px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #00a651 0%, #008f45 100%);
            color: white;
        }
        
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 166, 81, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .progress-container {
            display: none;
            margin: 30px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .status-text {
            text-align: center;
            color: #666;
            margin: 10px 0;
            font-size: 14px;
        }
        
        .results-container {
            display: none;
            margin-top: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #e0e0e0;
        }
        
        th {
            background: #667eea;
            color: white;
            font-weight: bold;
        }
        
        tr:hover {
            background: #f8f9ff;
        }
        
        .actions {
            text-align: center;
            margin: 30px 0;
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: none;
        }
        
        .success-message {
            background: #efe;
            color: #3c3;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: none;
        }
        
        .preview-image {
            max-width: 300px;
            max-height: 200px;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            margin: 10px;
        }
        
        .ocr-result {
            background: #f8f9ff;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 13px;
            white-space: pre-wrap;
            border: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🆔 استخراج بيانات البطاقات الشخصية</h1>
        <p class="subtitle">استخراج تلقائي من PDF أو صور - بدون API Key - مجاني 100%</p>
        
        <!-- منطقة الرفع -->
        <div class="upload-area" id="upload-area">
            <div class="upload-icon">📄</div>
            <div class="upload-text">اسحب ملف PDF أو صور البطاقات هنا</div>
            <div class="upload-hint">أو اضغط لاختيار ملف (PDF, JPG, PNG)</div>
            <input type="file" id="file-input" accept=".pdf,.jpg,.jpeg,.png" multiple>
        </div>
        
        <!-- أزرار التحكم -->
        <div class="actions">
            <button class="btn btn-primary" id="start-btn" onclick="startProcessing()" disabled>
                🔍 بدء الاستخراج
            </button>
            <button class="btn btn-success" id="download-btn" onclick="downloadExcel()" style="display:none;">
                📊 تحميل Excel
            </button>
        </div>
        
        <!-- شريط التقدم -->
        <div class="progress-container" id="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill">0%</div>
            </div>
            <div class="status-text" id="status-text">جاري التحميل...</div>
        </div>
        
        <!-- رسائل الخطأ والنجاح -->
        <div class="error-message" id="error-message"></div>
        <div class="success-message" id="success-message"></div>
        
        <!-- النتائج -->
        <div class="results-container" id="results-container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="total-cards">0</div>
                    <div class="stat-label">إجمالي البطاقات</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="extracted-cards">0</div>
                    <div class="stat-label">تم استخراجها</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="failed-cards">0</div>
                    <div class="stat-label">فشلت</div>
                </div>
            </div>
            
            <h3 style="margin: 20px 0; color: #333;"> البيانات المستخرجة</h3>
            <div id="table-container"></div>
        </div>
    </div>

    <script>
        // تهيئة PDF.js
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        
        let extractedData = [];
        let uploadedFiles = [];
        
        // معالجة السحب والإفلات
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });
        
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
        
        function handleFiles(files) {
            uploadedFiles = Array.from(files);
            document.getElementById('start-btn').disabled = false;
            showMessage('success', `✅ تم اختيار ${files.length} ملف(ات) بنجاح`);
        }
        
        async function startProcessing() {
            if (uploadedFiles.length === 0) {
                showMessage('error', '️ يرجى اختيار ملف أولاً');
                return;
            }
            
            document.getElementById('progress-container').style.display = 'block';
            document.getElementById('results-container').style.display = 'none';
            document.getElementById('download-btn').style.display = 'none';
            document.getElementById('start-btn').disabled = true;
            
            extractedData = [];
            
            try {
                for (let i = 0; i < uploadedFiles.length; i++) {
                    const file = uploadedFiles[i];
                    updateProgress((i / uploadedFiles.length) * 100, `جاري معالجة الملف ${i + 1} من ${uploadedFiles.length}...`);
                    
                    if (file.type === 'application/pdf') {
                        await processPDF(file);
                    } else if (file.type.startsWith('image/')) {
                        await processImage(file);
                    }
                }
                
                updateProgress(100, 'اكتمل الاستخراج!');
                displayResults();
                showMessage('success', `🎉 تم استخراج بيانات ${extractedData.length} بطاقة بنجاح!`);
                
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', '❌ حدث خطأ: ' + error.message);
            } finally {
                document.getElementById('start-btn').disabled = false;
            }
        }
        
        async function processPDF(file) {
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
            const totalPages = pdf.numPages;
            
            for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
                updateProgress(
                    ((pageNum - 1) / totalPages) * 100,
                    `جاري قراءة صفحة ${pageNum} من ${totalPages}...`
                );
                
                const page = await pdf.getPage(pageNum);
                const viewport = page.getViewport({ scale: 2.0 });
                
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                
                await page.render({
                    canvasContext: context,
                    viewport: viewport
                }).promise;
                
                const imageData = canvas.toDataURL('image/png');
                await extractDataFromImage(imageData, `صفحة ${pageNum}`);
            }
        }
        
        async function processImage(file) {
            const imageData = await fileToDataURL(file);
            await extractDataFromImage(imageData, file.name);
        }
        
        async function extractDataFromImage(imageData, source) {
            try {
                const result = await Tesseract.recognize(imageData, 'ara+eng', {
                    logger: m => {
                        if (m.status === 'recognizing text') {
                            updateProgress(m.progress * 100, `جاري قراءة النص... ${Math.round(m.progress * 100)}%`);
                        }
                    }
                });
                
                const text = result.data.text;
                const parsedData = parseCardData(text, source);
                
                if (parsedData) {
                    extractedData.push(parsedData);
                }
                
            } catch (error) {
                console.error('OCR Error:', error);
            }
        }
        
        function parseCardData(text, source) {
            // استخراج الرقم القومي (14 رقم)
            const nationalIdMatch = text.match(/\b(\d{14})\b/);
            
            // استخراج الاسم (عادة بعد كلمة الاسم أو في السطر الأول)
            const nameMatch = text.match(/(?:الاسم|Name)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج العنوان
            const addressMatch = text.match(/(?:العنوان|Address)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج تاريخ الميلاد
            const birthDateMatch = text.match(/(?:تاريخ الميلاد|Date of Birth)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج الحالة الاجتماعية
            const maritalStatusMatch = text.match(/(?:الحالة الاجتماعية|Marital Status)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج الديانة
            const religionMatch = text.match(/(?:الديانة|Religion)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج الوظيفة
            const jobMatch = text.match(/(?:الوظيفة|Job|Occupation)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج الجنس
            const genderMatch = text.match(/(?:الجنس|Sex|Gender)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج المحافظة
            const governorateMatch = text.match(/(?:محافظة|Governorate)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج محل الميلاد
            const birthPlaceMatch = text.match(/(?:محل الميلاد|Place of Birth)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج تاريخ الإصدار
            const issueDateMatch = text.match(/(?:تاريخ الإصدار|Issue Date)[:\s]*(.+?)(?:\n|$)/i);
            
            // استخراج تاريخ الانتهاء
            const expiryDateMatch = text.match(/(?:تاريخ الانتهاء|Expiry Date)[:\s]*(.+?)(?:\n|$)/i);
            
            // إذا لم نجد رقم قومي، نعتبر البطاقة غير صالحة
            if (!nationalIdMatch) {
                return null;
            }
            
            return {
                'الرقم القومي': nationalIdMatch[1],
                'الاسم': nameMatch ? nameMatch[1].trim() : '',
                'العنوان': addressMatch ? addressMatch[1].trim() : '',
                'تاريخ الميلاد': birthDateMatch ? birthDateMatch[1].trim() : '',
                'الحالة الاجتماعية': maritalStatusMatch ? maritalStatusMatch[1].trim() : '',
                'الديانة': religionMatch ? religionMatch[1].trim() : '',
                'الوظيفة': jobMatch ? jobMatch[1].trim() : '',
                'الجنس': genderMatch ? genderMatch[1].trim() : '',
                'المحافظة': governorateMatch ? governorateMatch[1].trim() : '',
                'محل الميلاد': birthPlaceMatch ? birthPlaceMatch[1].trim() : '',
                'تاريخ الإصدار': issueDateMatch ? issueDateMatch[1].trim() : '',
                'تاريخ الانتهاء': expiryDateMatch ? expiryDateMatch[1].trim() : '',
                'المصدر': source
            };
        }
        
        function displayResults() {
            document.getElementById('results-container').style.display = 'block';
            document.getElementById('download-btn').style.display = 'inline-block';
            
            document.getElementById('total-cards').textContent = uploadedFiles.length;
            document.getElementById('extracted-cards').textContent = extractedData.length;
            document.getElementById('failed-cards').textContent = uploadedFiles.length - extractedData.length;
            
            if (extractedData.length === 0) {
                document.getElementById('table-container').innerHTML = '<p style="text-align:center; color:#666;">لم يتم استخراج أي بيانات</p>';
                return;
            }
            
            // إنشاء جدول
            const columns = Object.keys(extractedData[0]);
            let tableHTML = '<table><thead><tr>';
            columns.forEach(col => {
                tableHTML += `<th>${col}</th>`;
            });
            tableHTML += '</tr></thead><tbody>';
            
            extractedData.forEach(row => {
                tableHTML += '<tr>';
                columns.forEach(col => {
                    tableHTML += `<td>${row[col] || ''}</td>`;
                });
                tableHTML += '</tr>';
            });
            
            tableHTML += '</tbody></table>';
            document.getElementById('table-container').innerHTML = tableHTML;
        }
        
        function downloadExcel() {
            if (extractedData.length === 0) {
                showMessage('error', '⚠️ لا توجد بيانات للتحميل');
                return;
            }
            
            const ws = XLSX.utils.json_to_sheet(extractedData);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, 'البطاقات المستخرجة');
            
            const fileName = `بطاقات_مستخرجة_${new Date().toISOString().split('T')[0]}.xlsx`;
            XLSX.writeFile(wb, fileName);
            
            showMessage('success', `📊 تم تحميل ملف Excel بنجاح: ${fileName}`);
        }
        
        function updateProgress(percent, message) {
            const progressFill = document.getElementById('progress-fill');
            const statusText = document.getElementById('status-text');
            
            progressFill.style.width = percent + '%';
            progressFill.textContent = Math.round(percent) + '%';
            statusText.textContent = message;
        }
        
        function showMessage(type, message) {
            const errorDiv = document.getElementById('error-message');
            const successDiv = document.getElementById('success-message');
            
            if (type === 'error') {
                errorDiv.textContent = message;
                errorDiv.style.display = 'block';
                successDiv.style.display = 'none';
                setTimeout(() => errorDiv.style.display = 'none', 5000);
            } else {
                successDiv.textContent = message;
                successDiv.style.display = 'block';
                errorDiv.style.display = 'none';
                setTimeout(() => successDiv.style.display = 'none', 5000);
            }
        }
        
        function fileToDataURL(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        }
    </script>
</body>
</html>

