# Saudi Aviation Analytics | تحليلات الطيران السعودي

لوحة معلومات تفاعلية باستخدام Streamlit لاستكشاف حركة الطيران في مطارات المملكة العربية السعودية خلال الفترة 2020–2025، مبنية باستخدام SQL وPython وPandas وPlotly.

An interactive Streamlit dashboard exploring Saudi airport air traffic from 2020–2025, built with SQL, Python, Pandas and Plotly.

## الإعداد والتشغيل | Setup

1. ضعي ملف `air_traffic.sqlite` في المجلد الرئيسي للمستودع بجانب ملف `app.py`.  
   Place `air_traffic.sqlite` in the repository root next to `app.py`.
2. على **Streamlit Community Cloud**، اختاري هذا المستودع والفرع `main` وملف التشغيل `app.py`.  
   On Streamlit Community Cloud select this repository, `main` branch, and entry point `app.py`.
3. أو شغّلي التطبيق محليًا:  
   Or run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## المميزات | Features

- مؤشرات المسافرين وحركات الطيران على مستوى المملكة.  
  National passenger and flight-movement indicators.
- ترتيب المطارات وحصصها النسبية والمقارنات السنوية.  
  Airport rankings, shares and year-over-year comparisons.
- التحليل الشهري باستخدام فلاتر تفاعلية.  
  Monthly analytics with interactive filters.
- مراجعة تغطية البيانات وجودتها.  
  Data-coverage and quality review.
- تصدير جداول التقارير بصيغة CSV.  
  CSV export of report tables.

## مصدر البيانات والمنهجية | Source and methodology

جُمعت البيانات من ملفات الحركة الجوية المنشورة للعموم من **الهيئة العامة للطيران المدني السعودية** للفترة 2020–2025. يختلف مستوى التفاصيل بين السنوات: بيانات 2022 سنوية، بينما تحتوي سنوات أخرى على تفاصيل شهرية. يجب توخي الحذر عند مقارنة الإجماليات الوطنية بسبب اختلاف تغطية المصادر أو نشاط المطارات. حركات الطيران ليست رحلات ذهاب وعودة فريدة، ومتوسط المسافرين لكل حركة لا يعادل نسبة إشغال المقاعد.

Compiled from publicly published Saudi General Authority of Civil Aviation air-traffic files covering 2020–2025. Source files vary by year: 2022 contains annual data, while other selected years have monthly detail. Use caution when comparing national totals across changing source coverage or airport activity. Flight movements are not unique round trips, and passengers per movement is not seat load factor.

## ملف البيانات | Data file

يحتوي `air_traffic.sqlite` (بحجم يقارب 12 ميجابايت) على جدول `air_traffic`، ويجب رفعه بصورة منفصلة إلى GitHub إذا لم يكن موجودًا.

`air_traffic.sqlite` (about 12 MB) contains the `air_traffic` table and must be added separately to GitHub if absent.
