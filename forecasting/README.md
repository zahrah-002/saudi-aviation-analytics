# Saudi Aviation | Time Series Forecasting

[English](#english) · [العربية](#arabic) · **[Open Interactive Dashboard](https://saudi-aviation-analytics-zahrah.streamlit.app/)**

<a id="english"></a>

## English

Passenger forecasting for **2026** using monthly observations from **January 2023–December 2025**. The interactive charts are integrated into the **Forecasting** section of the Streamlit application; no separate HTML viewer is required.

### Files

| File | Purpose |
| --- | --- |
| [`forecasting.py`](forecasting.py) | ADF, STL, 2025 holdout and rolling evaluation, ETS/SARIMA forecasts |
| [`Saudi_Aviation_Monthly_2023_2025_Forecasting.csv`](Saudi_Aviation_Monthly_2023_2025_Forecasting.csv) | 36 monthly historical observations |
| [`forecast_2026.csv`](forecast_2026.csv) | ETS and SARIMA projections, plus SARIMA 95% prediction intervals |
| [`Saudi_Aviation_PowerBI_Forecasting.csv`](Saudi_Aviation_PowerBI_Forecasting.csv) | 60 rows: 36 historical months and 24 model-specific forecast rows |
| [`model_performance_2025.csv`](model_performance_2025.csv) | Fixed 12-month holdout errors for the three models |
| `requirements.txt` | Forecasting dependencies |

### Method
Models are fitted on **2023–2024**, evaluated against **2025**, and refitted on **2023–2025** to forecast 2026. Methods include Seasonal Naive, additive ETS and SARIMA `(2,1,0)(1,0,0,12)`. Evaluation uses **MAE, RMSE and sMAPE**.

To reproduce from the repository root:
```bash
pip install -r forecasting/requirements.txt
python forecasting/forecasting.py
```
Output files are written to `forecasting/output/` locally.

**Interpretation:** These are unofficial statistical forecasts, not observed 2026 passenger totals. The 95% prediction intervals depend on SARIMA assumptions. With only 36 months of data and varying airport coverage, uncertainty is material. **Do not add ETS and SARIMA rows together** when calculating annual totals in Power BI.

---

<a id="arabic"></a>

## العربية

توقع أعداد المسافرين لعام **2026** باستخدام المشاهدات الشهرية من **يناير 2023 إلى ديسمبر 2025**. الرسوم البيانية التفاعلية مدمجة في قسم **Forecasting** داخل تطبيق Streamlit، ولا يلزم استخدام عارض HTML منفصل.

### الملفات

| الملف | الغرض |
| --- | --- |
| [`forecasting.py`](forecasting.py) | اختبار ADF، وتحليل STL، وتقييم الأداء على بيانات 2025 المحجوزة للاختبار، والتقييم المتحرك، وتوقعات ETS وSARIMA |
| [`Saudi_Aviation_Monthly_2023_2025_Forecasting.csv`](Saudi_Aviation_Monthly_2023_2025_Forecasting.csv) | 36 مشاهدة تاريخية شهرية |
| [`forecast_2026.csv`](forecast_2026.csv) | توقعات ETS وSARIMA، بالإضافة إلى فترات التنبؤ بنسبة 95% لنموذج SARIMA |
| [`Saudi_Aviation_PowerBI_Forecasting.csv`](Saudi_Aviation_PowerBI_Forecasting.csv) | 60 صفًا: 36 شهرًا من البيانات التاريخية و24 صفًا من التوقعات الخاصة بالنموذجين |
| [`model_performance_2025.csv`](model_performance_2025.csv) | أخطاء النماذج الثلاثة عند تقييمها على فترة اختبار ثابتة مدتها 12 شهرًا |
| `requirements.txt` | المكتبات اللازمة لتشغيل التنبؤ |

### المنهجية

تُلاءَم النماذج باستخدام بيانات **2023–2024**، ويُقيَّم أداؤها مقابل بيانات **2025**، ثم تُعاد ملاءمتها باستخدام بيانات **2023–2025** لإنتاج توقعات 2026. تشمل الطرق المستخدمة النموذج الموسمي الساذج (Seasonal Naive)، ونموذج ETS ذي المكونات الجمعية، ونموذج SARIMA بالمواصفات `(2,1,0)(1,0,0,12)`. ويُستخدم في التقييم كلٌّ من **MAE وRMSE وsMAPE**.

لإعادة تنفيذ التحليل من المجلد الرئيسي للمستودع:

```bash
pip install -r forecasting/requirements.txt
python forecasting/forecasting.py
```

تُحفَظ ملفات المخرجات محليًا في المجلد `forecasting/output/`.

**تفسير النتائج:** هذه النتائج توقعات إحصائية غير رسمية، وليست إجماليات فعلية مرصودة لأعداد المسافرين في عام 2026. وتعتمد فترات التنبؤ بنسبة 95% على افتراضات نموذج SARIMA. وبالنظر إلى أن البيانات تتضمن 36 شهرًا فقط مع تفاوت تغطية المطارات، فإن مستوى عدم اليقين يُعد مهمًا عند تفسير النتائج. **يجب عدم جمع صفوف توقعات ETS وSARIMA معًا** عند حساب الإجماليات السنوية في Power BI.
