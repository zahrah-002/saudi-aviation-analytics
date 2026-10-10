# Saudi Aviation Analytics | تحليلات الطيران السعودي

[العربية](#القسم-العربي) | [English](#english-section)

---

<a id="القسم-العربي"></a>

# القسم العربي

## نبذة عن المشروع

لوحة معلومات تفاعلية باستخدام Streamlit لاستكشاف حركة الطيران في مطارات المملكة العربية السعودية خلال الفترة **2020–2025**، مبنية باستخدام **SQL وPython وPandas وPlotly**.

## الإعداد والتشغيل

1. ضعي ملف `air_traffic.sqlite` في المجلد الرئيسي للمستودع بجانب ملف `app.py`.
2. على **Streamlit Community Cloud**، اختاري هذا المستودع والفرع `main` وملف التشغيل `app.py`.
3. أو شغّلي التطبيق محليًا باستخدام الأوامر التالية:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## المميزات

- مؤشرات المسافرين وحركات الطيران على مستوى المملكة.
- ترتيب المطارات وحصصها النسبية والمقارنات السنوية.
- التحليل الشهري باستخدام فلاتر تفاعلية.
- مراجعة تغطية البيانات وجودتها.
- تصدير جداول التقارير بصيغة CSV.

## مصدر البيانات والمنهجية

جُمعت البيانات من ملفات الحركة الجوية المنشورة للعموم من **الهيئة العامة للطيران المدني السعودية** للفترة **2020–2025**. يختلف مستوى التفاصيل بين السنوات: بيانات 2022 سنوية، بينما تحتوي سنوات أخرى على تفاصيل شهرية. يجب توخي الحذر عند مقارنة الإجماليات الوطنية بسبب اختلاف تغطية المصادر أو نشاط المطارات. حركات الطيران ليست رحلات ذهاب وعودة فريدة، ومتوسط المسافرين لكل حركة لا يعادل نسبة إشغال المقاعد.

## ملف البيانات

يحتوي `air_traffic.sqlite` (بحجم يقارب 12 ميجابايت) على جدول `air_traffic`، ويجب رفعه بصورة منفصلة إلى GitHub إذا لم يكن موجودًا.

---

<a id="english-section"></a>

# English Section

## About the Project

An interactive Streamlit dashboard exploring Saudi airport air traffic from **2020–2025**, built with **SQL, Python, Pandas and Plotly**.

## Setup

1. Place `air_traffic.sqlite` in the repository root next to `app.py`.
2. On **Streamlit Community Cloud**, select this repository, the `main` branch, and entry point `app.py`.
3. Or run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

- National passenger and flight-movement indicators.
- Airport rankings, shares and year-over-year comparisons.
- Monthly analytics with interactive filters.
- Data-coverage and quality review.
- CSV export of report tables.

## Source and Methodology

Compiled from publicly published **Saudi General Authority of Civil Aviation** air-traffic files covering **2020–2025**. Source files vary by year: 2022 contains annual data, while other selected years have monthly detail. Use caution when comparing national totals across changing source coverage or airport activity. Flight movements are not unique round trips, and passengers per movement is not seat load factor.

## Data File

`air_traffic.sqlite` (about 12 MB) contains the `air_traffic` table and must be added separately to GitHub if absent.
