# Saudi Aviation | Time Series Forecasting & Analytics

[English](#english) · [العربية](#arabic)

## English

This folder contains a **separate forecasting phase** of the Saudi Aviation Analytics portfolio project. The same repository's Streamlit dashboard has a separate **Forecasting** page while retaining its existing analysis sections.

### Contents
- `forecasting.py` — reproducible Python code for ADF, STL decomposition, 2025 holdout and expanding-window tests, Seasonal Naive / ETS / SARIMA, 2026 forecasts, SARIMA 95% prediction intervals, and CSV exports.
- `Saudi_Aviation_Monthly_2023_2025_Forecasting.csv` — monthly observations used in the analysis (36 rows, January 2023–December 2025).
- `requirements.txt` — dependencies.
- `forecast_2026.csv` — fixed 2026 ETS and SARIMA predictions plus SARIMA 95% intervals, used in the Streamlit forecasting page.
- [`Saudi_Aviation_PowerBI_Forecasting.csv`](Saudi_Aviation_PowerBI_Forecasting.csv) — 60 rows for Power BI: 36 actual monthly observations (2023–2025), plus 12 ETS and 12 SARIMA monthly projections (2026), with SARIMA prediction interval bounds.
- [`model_performance_2025.csv`](model_performance_2025.csv) — SARIMA, ETS and Seasonal Naive evaluation metrics (sMAPE, RMSE and MAE) for the fixed 2025 holdout.
- `output/` — generated when running the script; contains model scores, backtests and the Power BI-ready file.

### Run locally
From the repository root:

```bash
pip install -r forecasting/requirements.txt
python forecasting/forecasting.py
```

To run in **Google Colab**, upload `forecasting.py` and the CSV into the same directory, install the dependencies, and run `%run forecasting.py`.

### Methods and interpretation
Training: January 2023–December 2024. Holdout: January–December 2025. The fixed SARIMA specification is `(2,1,0)(1,0,0,12)` and ETS has additive trend/seasonality. Rolling one-month-ahead evaluation differs from the fixed 12-month forecast test. The final model forecasts 2026 after training on all 36 months.

Forecast intervals are model-based **prediction intervals**, not guarantees. Only 3 years of monthly data are available. The `airports_with_records` field varies (27–29) and even month-complete source files need not capture every operational category; 2022 is annual-only and excluded from monthly fitting. These projections are not official forecasts. **2026 forecast values must never be presented as actual observations.** Do not sum ETS and SARIMA scenario rows into one 2026 total in Power BI.

## العربية

يحتوي هذا المجلد على **مرحلة التنبؤ بالسلاسل الزمنية** ضمن مشروع تحليلات الطيران السعودي، وأصبح لها قسم «التنبؤ بحركة الطيران» داخل لوحة Streamlit السابقة دون تغيير الأقسام الأصلية.

يشمل الكود: اختبار ADF، تفكيك STL، مقارنة Seasonal Naive وETS وSARIMA على بيانات 2025، الاختبار المتحرك للشهر التالي، توقعات 2026، فترات التنبؤ 95%، وتصدير ملفات مناسبة لـPower BI.

**ملفات Power BI:** يتوفر ملف [`Saudi_Aviation_PowerBI_Forecasting.csv`](Saudi_Aviation_PowerBI_Forecasting.csv) الذي يجمع 36 شهرًا من البيانات الفعلية (2023–2025) مع توقعات النموذجين لعام 2026 (24 صفًا)، بالإضافة إلى [`model_performance_2025.csv`](model_performance_2025.csv) لمقارنة أداء النماذج على بيانات اختبار 2025. لا تُجمع توقعات ETS وSARIMA معًا عند حساب إجمالي 2026.

**التنفيذ:** تثبيت المكتبات من `forecasting/requirements.txt` ثم تشغيل `python forecasting/forecasting.py` من جذر المستودع.

**تنبيه منهجي:** تتوفر 36 مشاهدة شهرية من 2023 إلى 2025، مع تفاوت عدد المطارات التي لها سجلات. بيانات 2022 سنوية ولا تدخل النمذجة الشهرية. جميع أرقام 2026 توقعات استكشافية وليست نتائج رسمية فعلية، ويجب الفصل بين سيناريوهَي ETS وSARIMA في Power BI.
