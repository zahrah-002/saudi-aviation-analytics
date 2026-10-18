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

<table dir="rtl">
  <thead>
    <tr>
      <th align="right">الملف</th>
      <th align="right">الغرض</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td dir="ltr"><a href="forecasting.py"><code>forecasting.py</code></a></td>
      <td dir="rtl" align="right">اختبار <bdi dir="ltr">ADF</bdi>، وتحليل <bdi dir="ltr">STL</bdi>، وتقييم الأداء على بيانات عام 2025 المخصصة للاختبار، والتقييم المتحرك، وإنتاج توقعات <bdi dir="ltr">ETS</bdi> و<bdi dir="ltr">SARIMA</bdi>.</td>
    </tr>
    <tr>
      <td dir="ltr"><a href="Saudi_Aviation_Monthly_2023_2025_Forecasting.csv"><code>Saudi_Aviation_Monthly_2023_2025_Forecasting.csv</code></a></td>
      <td dir="rtl" align="right">36 مشاهدة شهرية تاريخية.</td>
    </tr>
    <tr>
      <td dir="ltr"><a href="forecast_2026.csv"><code>forecast_2026.csv</code></a></td>
      <td dir="rtl" align="right">توقعات <bdi dir="ltr">ETS</bdi> و<bdi dir="ltr">SARIMA</bdi>، بالإضافة إلى فترات التنبؤ بنسبة 95% لنموذج <bdi dir="ltr">SARIMA</bdi>.</td>
    </tr>
    <tr>
      <td dir="ltr"><a href="Saudi_Aviation_PowerBI_Forecasting.csv"><code>Saudi_Aviation_PowerBI_Forecasting.csv</code></a></td>
      <td dir="rtl" align="right">60 صفًا: 36 صفًا للبيانات الشهرية التاريخية، و24 صفًا للتوقعات الخاصة بالنموذجين.</td>
    </tr>
    <tr>
      <td dir="ltr"><a href="model_performance_2025.csv"><code>model_performance_2025.csv</code></a></td>
      <td dir="rtl" align="right">أخطاء النماذج الثلاثة خلال فترة اختبار ثابتة مدتها 12 شهرًا.</td>
    </tr>
    <tr>
      <td dir="ltr"><code>requirements.txt</code></td>
      <td dir="rtl" align="right">المكتبات البرمجية اللازمة لتشغيل التنبؤ.</td>
    </tr>
  </tbody>
</table>

### المنهجية

تُلاءَم النماذج باستخدام بيانات **2023–2024**، ويُقيَّم أداؤها مقابل بيانات **2025**، ثم تُعاد ملاءمتها باستخدام بيانات **2023–2025** لإنتاج توقعات 2026. تشمل الطرق المستخدمة النموذج الموسمي الساذج (Seasonal Naive)، ونموذج ETS ذي المكونات الجمعية، ونموذج SARIMA بالمواصفات `(2,1,0)(1,0,0,12)`. ويُستخدم في التقييم كلٌّ من **MAE وRMSE وsMAPE**.

لإعادة تنفيذ التحليل من المجلد الرئيسي للمستودع:

```bash
pip install -r forecasting/requirements.txt
python forecasting/forecasting.py
```

تُحفَظ ملفات المخرجات محليًا في المجلد `forecasting/output/`.

**تفسير النتائج:** هذه النتائج توقعات إحصائية غير رسمية، وليست إجماليات فعلية مرصودة لأعداد المسافرين في عام 2026. وتعتمد فترات التنبؤ بنسبة 95% على افتراضات نموذج SARIMA. وبالنظر إلى أن البيانات تتضمن 36 شهرًا فقط مع تفاوت تغطية المطارات، فإن مستوى عدم اليقين يُعد مهمًا عند تفسير النتائج. **يجب عدم جمع صفوف توقعات ETS وSARIMA معًا** عند حساب الإجماليات السنوية في Power BI.
