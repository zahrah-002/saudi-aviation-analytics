# Saudi Aviation Analytics | تحليلات الطيران السعودي

[English](#english) · [العربية](#arabic)

**[Live Dashboard](https://saudi-aviation-analytics-zahrah.streamlit.app/)** · **[Forecasting & Results](forecasting/README.md)** · **[GACA Open Data](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)**

---

<a id="english"></a>

## English

### Overview
Analysis of Saudi aviation traffic from **2020–2025**, using data published by the General Authority of Civil Aviation (GACA). The project combines **Python, SQL, SQLite, Plotly, and Streamlit** to examine passenger traffic, flight movements, airport rankings, annual comparisons, and monthly trends.

A dedicated forecasting section evaluates **Seasonal Naive, ETS, and SARIMA** on 2025 data, then produces **unofficial passenger forecasts for 2026**. The interactive Streamlit dashboard includes actual-versus-forecast trends, SARIMA 95% prediction intervals, and model error comparisons. A separate **Power BI** report was prepared for portfolio presentation.

### Dashboard sections
- **National Overview** — annual indicators and trends
- **Airport Performance** — rankings, shares, and 2024–2025 comparisons
- **Monthly Trends** — selected years and passenger/flight-movement trends
- **Forecasting** — 2026 projections, interactive charts, and evaluation metrics
- **Data Quality** — coverage and missing-value checks

### Files and methods
- `app.py`, `air_traffic.sqlite`, `requirements.txt` — Streamlit dashboard and processed database
- [Forecasting folder](forecasting/README.md) — Python analysis, source series, 2026 results, and Power BI-ready CSV files

**Run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Methodology:** The 2022 source has annual granularity; the other included years provide monthly records. Source scope and airport coverage can vary, so cross-year totals are not necessarily directly comparable. Forecast models use 36 monthly observations (2023–2025), with 2025 held out for evaluation. The 2026 figures and SARIMA intervals are **model-based, unofficial forecasts**, not actual passenger counts or official GACA projections.

**Source:** [GACA Open Data Library](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)

---

<a id="arabic"></a>

## العربية

### نبذة عن المشروع
مشروع لتحليل حركة الطيران في المملكة العربية السعودية خلال **2020–2025** باستخدام البيانات المنشورة من الهيئة العامة للطيران المدني (GACA). يجمع المشروع بين **Python وSQL وSQLite وPlotly وStreamlit** لاستعراض أعداد المسافرين وحركات الطيران، وترتيب المطارات، والمقارنات السنوية، والاتجاهات الشهرية.

يتضمن المشروع قسمًا للتنبؤ بأعداد المسافرين في **2026** باستخدام نماذج **Seasonal Naive وETS وSARIMA**، بعد تقييم أدائها على بيانات 2025. وتعرض لوحة Streamlit رسومًا تفاعلية لمقارنة القيم الفعلية والتوقعات وفترات تنبؤ SARIMA وأخطاء النماذج. كما أُعد تقرير منفصل باستخدام **Power BI** للعرض ضمن ملف الأعمال.

### أقسام لوحة المعلومات
- **النظرة الوطنية:** المؤشرات والاتجاهات السنوية
- **أداء المطارات:** الترتيب والحصص والمقارنة بين 2024 و2025
- **الحركة الشهرية:** اتجاهات المسافرين وحركات الطيران حسب السنوات المحددة
- **التنبؤ:** توقعات 2026 والرسوم التفاعلية وتقييم النماذج
- **جودة البيانات:** تغطية السجلات والقيم المفقودة

### الملفات والمنهجية
- `app.py` و`air_traffic.sqlite` و`requirements.txt`: تطبيق Streamlit وقاعدة البيانات المجمّعة
- [قسم التنبؤ والنتائج](forecasting/README.md): كود Python وبيانات السلسلة الشهرية وتوقعات 2026 وملفات CSV الجاهزة لـPower BI

**التشغيل محليًا:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**ملاحظة منهجية:** تتوفر بيانات 2022 بتفاصيل سنوية، بينما تشمل السنوات الأخرى المختارة بيانات شهرية. وقد تختلف تغطية المطارات ونطاق الملفات بين السنوات، لذلك تُفسَّر المقارنات بحذر. تعتمد نماذج التنبؤ على 36 مشاهدة شهرية خلال 2023–2025، مع تقييم الأداء على 2025. نتائج 2026 وفترات تنبؤ SARIMA **توقعات إحصائية غير رسمية** وليست بيانات فعلية أو توقعات صادرة عن الهيئة.

**المصدر:** [مكتبة البيانات المفتوحة — الهيئة العامة للطيران المدني](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)
