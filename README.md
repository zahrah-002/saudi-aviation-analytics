# Saudi Aviation Analytics | تحليلات الطيران السعودي

[العربية](#arabic-section) · [English](#english-section)

---

<a id="arabic-section"></a>

# النسخة العربية

## نبذة عن المشروع

**تحليلات الطيران السعودي** مشروع لتحليل بيانات الحركة الجوية في مطارات المملكة العربية السعودية خلال الفترة **2020–2025**. يقدم لوحة معلومات تفاعلية لاستكشاف أعداد المسافرين وحركات الطيران، ومقارنة أداء المطارات، ودراسة الاتجاهات الزمنية باستخدام **SQL وPython وPandas وPlotly وStreamlit**.

## محتوى لوحة المعلومات

- **نظرة وطنية:** مؤشرات إجمالية للمسافرين وحركات الطيران والمطارات.
- **أداء المطارات:** ترتيب المطارات، وحصصها النسبية، ومقارنة التغير السنوي.
- **التحليل الشهري:** استكشاف تطور الحركة الجوية باستخدام فلاتر تفاعلية.
- **جودة البيانات:** مراجعة التغطية الزمنية، ومستويات التفاصيل، والقيم المفقودة.
- **تصدير النتائج:** إتاحة الجداول التحليلية بصيغة CSV.

## التقنيات المستخدمة

**SQL · Python · Pandas · Plotly · Streamlit · SQLite**

## هيكل المشروع والتشغيل

يتضمن المشروع ملف التطبيق `app.py`، وملف المتطلبات البرمجية `requirements.txt`، وقاعدة بيانات SQLite باسم `air_traffic.sqlite`. يعتمد تشغيل التطبيق على وجود الملفات الثلاثة في المجلد الرئيسي للمشروع.

يتوفر نشر التطبيق عبر **Streamlit Community Cloud** بالاعتماد على مستودع GitHub، والفرع `main`، وملف الدخول `app.py`. كما يدعم التشغيل محليًا بعد تثبيت المكتبات المطلوبة:

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **حالة البيانات:** ملف `air_traffic.sqlite` مطلوب لتشغيل اللوحة، ويُضاف بصورة منفصلة إلى المستودع عند عدم توفره.

## مصدر البيانات والمنهجية

يعتمد المشروع على ملفات الحركة الجوية المنشورة من **الهيئة العامة للطيران المدني السعودية (GACA)** للفترة **2020–2025**. تختلف مستويات تفاصيل البيانات بين السنوات؛ إذ تتوفر بيانات **2022** على المستوى السنوي، بينما تتضمن السنوات الأخرى المختارة تفاصيل شهرية. لذلك تُفسَّر المقارنات السنوية مع مراعاة اختلاف نطاق المصادر وتغطية المطارات.

تمثل حركات الطيران الحركات المسجلة وليست بالضرورة رحلات ذهاب وعودة مستقلة، كما أن متوسط المسافرين لكل حركة لا يعادل نسبة إشغال المقاعد. وتُعد المؤشرات المستخرجة نتائج تحليلية للبيانات المجمعة، وليست بديلًا عن المؤشرات الرسمية المنشورة.

---

<a id="english-section"></a>

# English Version

## Project Overview

**Saudi Aviation Analytics** is a data analytics project exploring air traffic across airports in Saudi Arabia from **2020 to 2025**. The interactive dashboard examines passenger volumes, flight movements, airport performance, and time-based trends using **SQL, Python, Pandas, Plotly, and Streamlit**.

## Dashboard Features

- **National overview:** Total passenger, flight-movement, and airport indicators.
- **Airport performance:** Airport rankings, passenger shares, and year-over-year comparisons.
- **Monthly analysis:** Interactive exploration of air-traffic trends.
- **Data quality:** Review of temporal coverage, granularity, and missing values.
- **Data export:** Downloadable analytical tables in CSV format.

## Technology Stack

**SQL · Python · Pandas · Plotly · Streamlit · SQLite**

## Project Structure and Deployment

The project consists of `app.py` for the application, `requirements.txt` for Python dependencies, and `air_traffic.sqlite` for the SQLite database. All three files are required in the project root for the application to run.

Deployment is supported through **Streamlit Community Cloud** using the GitHub repository, the `main` branch, and `app.py` as the entry point. Local execution is also supported after installing the dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Data file status:** The application requires `air_traffic.sqlite`. This file must be added separately to the repository if it is not already present.

## Data Source and Methodology

The project uses publicly available air-traffic datasets published by the **Saudi General Authority of Civil Aviation (GACA)** for **2020–2025**. Data granularity varies by year: **2022** is represented by annual data, whereas other selected years include monthly detail. Cross-year comparisons therefore require care regarding source scope and airport coverage.

Flight movements do not necessarily represent unique round trips, and passengers per movement is not equivalent to aircraft seat load factor. The resulting indicators describe the compiled dataset and should not be presented as substitutes for official published statistics.
