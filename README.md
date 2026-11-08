# Biotech FDA Catalyst Intelligence — MVP

نسخة أولية مجانية لمراقبة أسهم التكنولوجيا الحيوية الأمريكية وبناء قاعدة عمل قابلة للتوسع.

## ما تتضمنه النسخة
- واجهة Streamlit.
- قائمة مراقبة قابلة للتعديل.
- أسعار تاريخية ومؤشرات زخم/تذبذب أولية عبر yfinance.
- سجلات موافقات دوائية من openFDA Drugs@FDA.
- بحث التجارب السريرية عبر ClinicalTrials.gov API v2.
- ملف CSV لقائمة محفزات FDA لإدخال الأحداث الموثقة يدوياً.
- GitHub Actions لتشغيل فحص يومي ورفع تقرير CSV كـ Artifact.

## ما لا تتضمنه بعد
- لا يوجد مصدر مجاني موثوق وشامل لكل تواريخ PDUFA المستقبلية.
- لا يوجد حالياً نموذج احتمالية موافقة FDA؛ لا يجوز تفسير درجة الزخم كاحتمال موافقة.
- لا توجد بيانات خيارات أو إجماع EPS آني ضمن النسخة المجانية.
- بيانات yfinance مناسبة للنموذج الأولي وقد تتأخر أو تكون غير مكتملة؛ ليست بديلاً عن مزود سوق مرخص.

## التشغيل المحلي
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## النشر السحابي المجاني
1. أنشئ مستودع GitHub جديداً وارفع محتويات هذا المشروع.
2. افتح https://share.streamlit.io وسجّل الدخول بحساب GitHub.
3. اختر المستودع والفرع والملف `app.py`.
4. اضغط Deploy.
5. لا تحتاج مفاتيح API في النسخة الأولى.

## الفحص اليومي
ملف `.github/workflows/daily_scan.yml` يشغّل `scripts/daily_scan.py` أيام العمل ويرفع CSV كتقرير قابل للتنزيل من تبويب Actions في GitHub.

ملاحظة: جدولة GitHub Actions بتوقيت UTC، وقد تحتاج تعديل وقت cron بين التوقيت الصيفي والشتوي الأمريكي. كما أن GitHub قد يؤخر تشغيل المهام المجدولة.

## إدخال أحداث FDA موثقة
استخدم `data/catalysts_template.csv` وأضف:
- Ticker
- اسم الدواء
- نوع الحدث
- تاريخ الحدث
- حالة التاريخ: confirmed أو estimated
- رابط المصدر الأساسي

لا تضف تاريخاً اعتماداً على شائعة أو مصدر غير موثوق.

## مصادر البيانات
- openFDA Drugs@FDA: https://open.fda.gov/apis/drug/drugsfda/
- ClinicalTrials.gov API: https://clinicaltrials.gov/data-api/about-api
- SEC EDGAR: https://www.sec.gov/edgar/sec-api-documentation
- Yahoo Finance via yfinance: https://github.com/ranaroussi/yfinance

## تحذير
الأداة بحثية وليست نصيحة استثمارية. أحداث FDA قد تسبب فجوات سعرية حادة، وقد تخسر كامل رأس المال المستثمر في سهم صغير أو حدث ثنائي.
