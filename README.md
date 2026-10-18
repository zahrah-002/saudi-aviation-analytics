# Saudi Aviation Analytics | تحليلات الطيران السعودي

[English](#english-section) · [العربية](#arabic-section)

**[Live Interactive Dashboard](https://saudi-aviation-analytics-zahrah.streamlit.app/)** · **[Forecasting Analysis](forecasting/README.md)** · **[GACA Open Data](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)**

**[لوحة المعلومات التفاعلية](https://saudi-aviation-analytics-zahrah.streamlit.app/)** · **[تحليل التنبؤ](forecasting/README.md)** · **[مصدر البيانات الرسمي](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)**

> **Dashboard preview:** Open the live Streamlit dashboard using the link above. Power BI forecasting visuals are a separate portfolio deliverable; no public interactive Power BI report is linked here.

---

<a id="english-section"></a>

# English Version

## Project Overview

**Saudi Aviation Analytics** is a data analytics project exploring air traffic across airports in Saudi Arabia from **2020 to 2025**. The interactive dashboard examines passenger volumes, flight movements, airport performance, and time-based trends using **SQL, Python, Pandas, Plotly, and Streamlit**. The same project includes time-series forecasting in Python and a separate Power BI forecasting dashboard.

## Forecasting / التنبؤ بالسلاسل الزمنية

The independent **[Time Series Forecasting & Analytics](forecasting/README.md)** section contains the Python forecasting workflow, the monthly 2023–2025 dataset, model validation, and instructions for exporting to Power BI. The dashboard now also includes a **Forecasting** section displaying 2026 passenger projections, model comparisons, and SARIMA prediction intervals.

يتضمن قسم **[التنبؤ بالسلاسل الزمنية](forecasting/README.md)** أكواد Python وبيانات 2023–2025 الشهرية ومقارنة النماذج وتجهيز ملفات Power BI، مع عرض التوقعات أيضًا في قسم مستقل داخل لوحة Streamlit، دون تغيير أقسام التحليل السابقة.

## Dashboard Features

- **National overview:** Total passenger, flight-movement, and airport indicators.
- **Airport performance:** Airport rankings, passenger shares, and year-over-year comparisons.
- **Monthly analysis:** Interactive exploration of air-traffic trends.
- **Forecasting:** ETS and SARIMA passenger projections for 2026, model evaluation, and 95% SARIMA prediction intervals.
- **Data quality:** Review of temporal coverage, granularity, and missing values.
- **Data export:** Downloadable analytical tables in CSV format.

## Technology Stack

**SQL · Python · Pandas · Plotly · Streamlit · SQLite · Statsmodels · Power BI**

## Project Structure and Deployment

The project consists of `app.py` for the application, `requirements.txt` for Python dependencies, and `air_traffic.sqlite` for the SQLite database. All three files are required in the project root for the application to run.

Deployment is supported through **Streamlit Community Cloud** using the GitHub repository, the `main` branch, and `app.py` as the entry point. Local execution is also supported after installing the dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Data file status:** The `air_traffic.sqlite` database is included in this repository. It contains processed Saudi aviation traffic data for 2020–2025 and is used directly by the interactive dashboard.

## Data Source and Methodology

The project uses publicly available air-traffic datasets published by the **[Saudi General Authority of Civil Aviation (GACA)](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)** for **2020–2025**. Data granularity varies by year: **2022** is represented by annual data, whereas other selected years include monthly detail. Cross-year comparisons therefore require care regarding source scope and airport coverage.

Flight movements do not necessarily represent unique round trips, and passengers per movement is not equivalent to aircraft seat load factor. The resulting indicators describe the compiled dataset and should not be presented as substitutes for official published statistics.

---

<a id="arabic-section"></a>

# النسخة العربية

## نبذة عن المشروع

**تحليلات الطيران السعودي** مشروع لتحليل بيانات الحركة الجوية في مطارات المملكة العربية السعودية خلال الفترة **2020–2025**. يقدم لوحة معلومات تفاعلية لاستكشاف أعداد المسافرين وحركات الطيران، ومقارنة أداء المطارات، ودراسة الاتجاهات الزمنية باستخدام **SQL وPython وPandas وPlotly وStreamlit**. ويتضمن المشروع أيضًا التنبؤ بالسلاسل الزمنية باستخدام Python ولوحة منفصلة لتصور النتائج في Power BI.

## محتوى لوحة المعلومات

- **نظرة وطنية:** مؤشرات إجمالية للمسافرين وحركات الطيران والمطارات.
- **أداء المطارات:** ترتيب المطارات، وحصصها النسبية، ومقارنة التغير السنوي.
- **التحليل الشهري:** استكشاف تطور الحركة الجوية باستخدام فلاتر تفاعلية.
- **التنبؤ:** توقعات أعداد المسافرين لعام 2026 باستخدام ETS وSARIMA، ومقارنة النماذج وفترات تنبؤ SARIMA بنسبة 95%.
- **جودة البيانات:** مراجعة التغطية الزمنية، ومستويات التفاصيل، والقيم المفقودة.
- **تصدير النتائج:** إتاحة الجداول التحليلية بصيغة CSV.

## التقنيات المستخدمة

**SQL · Python · Pandas · Plotly · Streamlit · SQLite · Statsmodels · Power BI**

## هيكل المشروع والتشغيل

يتضمن المشروع ملف التطبيق `app.py`، وملف المتطلبات البرمجية `requirements.txt`، وقاعدة بيانات SQLite باسم `air_traffic.sqlite`. يعتمد تشغيل التطبيق على وجود الملفات الثلاثة في المجلد الرئيسي للمشروع.

يتوفر نشر التطبيق عبر **Streamlit Community Cloud** بالاعتماد على مستودع GitHub، والفرع `main`، وملف الدخول `app.py`. كما يدعم التشغيل محليًا بعد تثبيت المكتبات المطلوبة:

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **حالة البيانات:** تتوفر قاعدة بيانات `air_traffic.sqlite` ضمن المستودع، وتحتوي على بيانات حركة الطيران السعودي المجمّعة للفترة 2020–2025، وتُستخدم مباشرة في تشغيل لوحة المعلومات التفاعلية.

## مصدر البيانات والمنهجية

يعتمد المشروع على ملفات الحركة الجوية المنشورة من **[الهيئة العامة للطيران المدني السعودية (GACA)](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)** للفترة **2020–2025**. تختلف مستويات تفاصيل البيانات بين السنوات؛ إذ تتوفر بيانات **2022** على المستوى السنوي، بينما تتضمن السنوات الأخرى المختارة تفاصيل شهرية. لذلك تُفسَّر المقارنات السنوية مع مراعاة اختلاف نطاق المصادر وتغطية المطارات.

تمثل حركات الطيران الحركات المسجلة وليست بالضرورة رحلات ذهاب وعودة مستقلة، كما أن متوسط المسافرين لكل حركة لا يعادل نسبة إشغال المقاعد. وتُعد المؤشرات المستخرجة نتائج تحليلية للبيانات المجمعة، وليست بديلًا عن المؤشرات الرسمية المنشورة.
