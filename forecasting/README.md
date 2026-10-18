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

يعرض هذا القسم توقعات أعداد المسافرين لعام **2026** باستخدام 36 مشاهدة شهرية خلال **2023–2025**. الرسوم التفاعلية متاحة مباشرة في قسم **Forecasting** داخل لوحة Streamlit، دون الحاجة إلى ملف HTML منفصل.

**ملفات المشروع:** يحتوي المجلد على كود `forecasting.py`، والبيانات الشهرية التاريخية، وتوقعات النموذجين لعام 2026، وملف CSV مناسب لـPower BI، ونتائج مقارنة دقة النماذج على اختبار 2025. روابط الملفات موضحة في الجدول أعلاه.

**المنهجية:** تمت ملاءمة النماذج باستخدام بيانات 2023–2024 وتقييمها على 2025، ثم إعادة ملاءمتها ببيانات 2023–2025 لتوقع 2026. تشمل النماذج Seasonal Naive وETS وSARIMA، ومقاييس التقييم MAE وRMSE وsMAPE.

**ملاحظة:** النتائج توقعات إحصائية غير رسمية، وليست أعدادًا فعلية لعام 2026. تعتمد فترة التنبؤ بنسبة 95% على افتراضات SARIMA، وقد يؤثر قصر السلسلة واختلاف تغطية المطارات في الدقة. يجب عدم جمع توقعات ETS وSARIMA عند حساب الإجمالي السنوي في Power BI.
