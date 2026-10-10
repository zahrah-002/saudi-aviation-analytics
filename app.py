"""Interactive Saudi aviation dashboard with Arabic and English interfaces."""
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Saudi Aviation Analytics | تحليلات الطيران السعودي",
    page_icon="✈️",
    layout="wide",
)

DB_FILE = Path(__file__).resolve().parent / "air_traffic.sqlite"
MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTHS_AR = [
    "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
    "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
]
AIRPORT_NAMES = {
    "ABT": ("الباحة", "Al Baha"),
    "AHB": ("أبها", "Abha"),
    "AJF": ("الجوف", "Al Jouf"),
    "AQI": ("القيصومة", "Al Qaisumah"),
    "BHH": ("بيشة", "Bisha"),
    "DMM": ("الدمام", "Dammam"),
    "DWD": ("الدوادمي", "Dawadmi"),
    "EAM": ("نجران", "Najran"),
    "EJH": ("الوجه", "Al Wajh"),
    "ELQ": ("القصيم", "Qassim"),
    "GIZ": ("جازان", "Jazan"),
    "HAS": ("حائل", "Hail"),
    "HOF": ("الأحساء", "Al Ahsa"),
    "JED": ("جدة", "Jeddah"),
    "MED": ("المدينة المنورة", "Madinah"),
    "NUM": ("نيوم", "NEOM"),
    "RAE": ("عرعر", "Arar"),
    "RAH": ("رفحاء", "Rafha"),
    "RGB": ("رابغ", "Rabigh"),
    "RSI": ("البحر الأحمر", "Red Sea"),
    "RUH": ("الرياض", "Riyadh"),
    "SHW": ("شرورة", "Sharurah"),
    "TIF": ("الطائف", "Taif"),
    "TUI": ("طريف", "Turaif"),
    "TUU": ("تبوك", "Tabuk"),
    "ULH": ("العلا", "AlUla"),
    "URY": ("القريات", "Qurayyat"),
    "WAE": ("وادي الدواسر", "Wadi Al Dawasir"),
    "YNB": ("ينبع", "Yanbu"),
}
PALETTE = ["#2dd4bf", "#38bdf8", "#f59e0b", "#a78bfa", "#fb7185"]

WORDS = {
    "ar": {
        "title": "تحليلات الطيران السعودي",
        "subtitle": "مؤشرات حركة الطيران وأداء المطارات في المملكة العربية السعودية | 2020–2025",
        "language": "اللغة | Language",
        "navigation": "أقسام لوحة المعلومات",
        "national": "النظرة الوطنية",
        "airports": "أداء المطارات",
        "monthly": "الحركة الشهرية",
        "quality": "جودة البيانات",
        "filters": "فلاتر البيانات",
        "airport_filter": "المطارات",
        "all_airports": "جميع المطارات",
        "type_filter": "نوع الرحلة",
        "direction_filter": "الاتجاه",
        "domestic": "داخلية",
        "international": "دولية",
        "arrival": "وصول",
        "departure": "مغادرة",
        "source": "المصدر: ملفات الحركة الجوية المنشورة من الهيئة العامة للطيران المدني السعودية (2020–2025).",
        "missing_file": "ملف قاعدة البيانات air_traffic.sqlite غير موجود بجانب app.py في المستودع.",
        "missing_file_hint": "ملف قاعدة البيانات ضروري لعرض النتائج. يُضاف إلى المجلد الرئيسي للمستودع، ثم يُعاد تشغيل التطبيق.",
        "load_error": "تعذّر قراءة بيانات SQLite.",
        "no_results": "لا توجد نتائج مطابقة للفلاتر المحددة.",
        "national_title": "المؤشرات الوطنية",
        "indicator_year": "سنة المؤشرات",
        "passengers": "المسافرون",
        "movements": "حركات الطيران",
        "airports_count": "عدد المطارات",
        "passengers_per_movement": "مسافر لكل حركة",
        "passenger_trend": "تطور أعداد المسافرين",
        "movement_trend": "تطور حركات الطيران",
        "year": "السنة",
        "passenger_growth": "نمو المسافرين (%)",
        "movement_growth": "نمو حركات الطيران (%)",
        "annual_note": "ملاحظة منهجية: تتضمن بيانات 2022 مجاميع سنوية، في حين تتوفر تفاصيل شهرية في سنوات أخرى. تختلف تغطية المطارات ونطاق الملفات، لذلك يجب توخي الحذر عند مقارنة الإجماليات ومعدلات النمو السنوية.",
        "airport_title": "ترتيب المطارات",
        "select_two_airports": "يجب اختيار مجموعة مكوّنة من مطارين أو أكثر للمقارنة.",
        "one_airport_note": "تظهر بيانات المطار المحدد أدناه، وتُتاح المقارنة بين المطارات عند تحديد مطارين أو أكثر.",
        "national_growth_title": "مقارنة الأداء بين 2024 و2025",
        "passenger_yoy_kpi": "تغير أعداد المسافرين",
        "movement_yoy_kpi": "تغير حركات الطيران",
        "national_growth_note": "مقارنة استكشافية حسب الفلاتر المختارة، وتشمل {airports} مطارًا تتوفر لها سجلات في جميع أشهر 2024 و2025. اكتمال الأشهر لا يضمن اكتمال كل الفئات التشغيلية.",
        "type_comparison_title": "المسافرون حسب نوع الرحلة",
        "official_source_link": "مكتبة البيانات المفتوحة — الهيئة العامة للطيران المدني",
        "airport_name": "المطار",
        "show_count": "عدد المطارات المعروضة",
        "share_pct": "حصة المسافرين (%)",
        "download_ranking": "تحميل ترتيب المطارات CSV",
        "airport_comparison": "مقارنة المطارات: 2024 و2025",
        "twelve_months": "اقتصار المقارنة على المطارات التي لديها سجلات في الأشهر الـ12 في كلا العامين",
        "passengers_2024": "مسافرو 2024",
        "passengers_2025": "مسافرو 2025",
        "passenger_diff": "التغير في المسافرين",
        "growth_pct": "النمو (%)",
        "download_comparison": "تحميل مقارنة المطارات CSV",
        "insufficient_comparison": "لا توجد بيانات كافية للمقارنة وفق الخيارات الحالية.",
        "airport_note": "وجود سجلات للأشهر الاثني عشر لا يضمن اكتمال تغطية جميع فئات الرحلات أو اتجاهاتها.",
        "monthly_title": "التحليل الشهري",
        "years_filter": "سنوات العرض",
        "metric_select": "المؤشر",
        "choose_year": "يجب تحديد سنة واحدة على الأقل.",
        "month": "الشهر",
        "download_monthly": "تحميل البيانات الشهرية CSV",
        "monthly_note": "لا تُعرض بيانات 2022 في الرسم الشهري لأنها وردت بصورة سنوية. وتتطلب دراسة الموسمية فترة زمنية وتغطية متسقتين.",
        "quality_title": "جودة البيانات وتغطيتها",
        "records": "السجلات",
        "coverage_airports": "المطارات",
        "months_count": "الأشهر المسجلة",
        "missing_passengers": "قيم المسافرين المفقودة",
        "missing_movements": "قيم الحركات المفقودة",
        "granularity": "مستوى التفاصيل",
        "annual_level": "سنوي",
        "monthly_level": "شهري",
        "coverage_title": "تغطية الأشهر حسب المطار",
        "months_2024": "أشهر 2024",
        "months_2025": "أشهر 2025",
        "quality_note": "غياب سجل لشهر معين لا يعني بالضرورة توقف الرحلات، كما أن وجود سجل لا يثبت اكتمال جميع الفئات التشغيلية.",
    },
    "en": {
        "title": "Saudi Aviation Analytics",
        "subtitle": "Air Traffic Indicators and Airport Performance in Saudi Arabia | 2020–2025",
        "language": "Language | اللغة",
        "navigation": "Dashboard sections",
        "national": "National Overview",
        "airports": "Airport Performance",
        "monthly": "Monthly Trends",
        "quality": "Data Quality",
        "filters": "Data filters",
        "airport_filter": "Airports",
        "all_airports": "All airports",
        "type_filter": "Flight type",
        "direction_filter": "Direction",
        "domestic": "Domestic",
        "international": "International",
        "arrival": "Arrival",
        "departure": "Departure",
        "source": "Source: Saudi General Authority of Civil Aviation (GACA) air-traffic files, 2020–2025.",
        "missing_file": "Database file air_traffic.sqlite is missing beside app.py in the repository.",
        "missing_file_hint": "The database is required to display results. Add it to the repository root, then restart the application.",
        "load_error": "Could not read the SQLite data.",
        "no_results": "No data matches the selected filters.",
        "national_title": "National Overview",
        "indicator_year": "Indicator year",
        "passengers": "Passengers",
        "movements": "Flight Movements",
        "airports_count": "Airports",
        "passengers_per_movement": "Passengers per movement",
        "passenger_trend": "Passenger Trend",
        "movement_trend": "Flight Movement Trend",
        "year": "Year",
        "passenger_growth": "Passenger growth (%)",
        "movement_growth": "Flight movement growth (%)",
        "annual_note": "Methodology: 2022 contains annual aggregates, whereas other years include monthly detail. Airport coverage and source-file scopes vary, so comparisons of national totals and annual growth require care.",
        "airport_title": "Airport Rankings",
        "select_two_airports": "Select a group of at least two airports to compare.",
        "one_airport_note": "The selected airport's individual data is shown below. Select two or more airports for an airport-to-airport comparison.",
        "national_growth_title": "Performance Comparison: 2024 vs 2025",
        "passenger_yoy_kpi": "Passenger change",
        "movement_yoy_kpi": "Flight movement change",
        "national_growth_note": "Exploratory comparison based on the active filters, covering {airports} airports with records for all twelve months of 2024 and 2025. Monthly presence does not guarantee complete category coverage.",
        "type_comparison_title": "Passengers by Flight Type",
        "official_source_link": "GACA Open Data Library",
        "airport_name": "Airport",
        "show_count": "Airports to display",
        "share_pct": "Passenger share (%)",
        "download_ranking": "Download airport rankings CSV",
        "airport_comparison": "Airport Comparison: 2024 vs 2025",
        "twelve_months": "Only include airports with records in all 12 months for both years",
        "passengers_2024": "2024 passengers",
        "passengers_2025": "2025 passengers",
        "passenger_diff": "Passenger change",
        "growth_pct": "Growth (%)",
        "download_comparison": "Download airport comparison CSV",
        "insufficient_comparison": "Insufficient data for comparison under the selected filters.",
        "airport_note": "Records in all twelve months do not guarantee complete coverage of every flight category or direction.",
        "monthly_title": "Monthly Trends",
        "years_filter": "Years to display",
        "metric_select": "Metric",
        "choose_year": "Select at least one year.",
        "month": "Month",
        "download_monthly": "Download monthly data CSV",
        "monthly_note": "2022 is excluded from monthly charts because it contains annual aggregates. Assessing seasonality requires a consistent period and data coverage.",
        "quality_title": "Data Quality and Coverage",
        "records": "Records",
        "coverage_airports": "Airports",
        "months_count": "Months represented",
        "missing_passengers": "Missing passenger values",
        "missing_movements": "Missing movement values",
        "granularity": "Granularity",
        "annual_level": "Annual",
        "monthly_level": "Monthly",
        "coverage_title": "Monthly Airport Coverage",
        "months_2024": "Months in 2024",
        "months_2025": "Months in 2025",
        "quality_note": "Missing monthly records do not necessarily mean operations stopped, and recorded months do not establish complete operational coverage.",
    },
}

# Language choice is saved across page navigations.
with st.sidebar:
    language = st.radio(
        "اللغة | Language",
        options=["ar", "en"],
        format_func=lambda x: "العربية" if x == "ar" else "English",
        horizontal=True,
        key="dashboard_language",
    )
T = WORDS[language]
RTL = language == "ar"
dir_attr = "rtl" if RTL else "ltr"
align = "right" if RTL else "left"


def airport_label(code):
    found = AIRPORT_NAMES.get(code)
    return (found[0] if RTL else found[1]) if found else str(code)


def number(value, digits=0):
    return f"{value:,.{digits}f}" if pd.notna(value) else "—"


def render_kpis(items):
    """Responsive card grid preserves the entire numeric string on all devices."""
    cards = []
    for label, value in items:
        cards.append(
            '<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value" dir="ltr">{value}</div>'
            '</div>'
        )
    st.markdown(
        '<div class="kpi-grid">' + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )


def figure(fig, height=410):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color="#dcecf5"),
        margin=dict(t=45, b=35, l=20, r=20),
        legend=dict(orientation="h", y=1.16),
        hovermode="closest",
    )
    st.plotly_chart(fig, use_container_width=True)


def info_note(message):
    st.markdown(f'<div class="info-note">{message}</div>', unsafe_allow_html=True)


st.markdown(
    """
<style>
.stApp {background:#0c1628; color:#edf7ff; font-family:Arial,"Segoe UI",sans-serif}
[data-testid="stSidebar"] {background:#122139}
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
.stApp h1, .stApp h2, .stApp h3, .stApp p {
  font-family:Arial,"Segoe UI",sans-serif !important;
}
.block-container {padding-top:1.5rem; max-width:1350px}
[data-testid="stAppViewContainer"] .block-container {
  direction:__DIR__;
  text-align:__ALIGN__;
}
[data-testid="stSidebar"] {
  direction:__DIR__;
  text-align:__ALIGN__;
}
h1,h2,h3 {letter-spacing:-.012em}
.hero {
  background:linear-gradient(115deg,#133b52,#18304a 65%,#1a2341);
  border:1px solid #35546a; border-radius:20px;
  padding:23px 26px; margin:5px 0 24px;
  direction:__DIR__; text-align:__ALIGN__;
}
.hero h1 {margin:0; color:#f2faff; font-size:clamp(1.45rem,2.5vw,2rem)}
.hero p {margin:8px 0 0; color:#b6d8e8; line-height:1.7}
.kpi-grid {
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(min(100%, 228px), 1fr));
  gap:14px; margin:18px 0 30px;
  direction:__DIR__;
}
.kpi-card {
  min-width:0; background:#162a44; border:1px solid #314863;
  border-radius:16px; padding:20px 19px; min-height:130px;
  display:flex; flex-direction:column; justify-content:center;
}
.kpi-label {
  font-size:.91rem; color:#c9def0; line-height:1.5;
  margin-bottom:13px; text-align:__ALIGN__; font-weight:500;
}
.kpi-value {
  display:block; width:100%; font-size:clamp(1.23rem,1.85vw,1.85rem);
  font-weight:750; line-height:1.3; font-variant-numeric:tabular-nums;
  color:#fff; letter-spacing:-.028em;
  text-align:__ALIGN__; white-space:nowrap;
  overflow:visible; text-overflow:clip;
}
.info-note {
  background:#182e49; border-inline-start:3px solid #38bdf8;
  border-radius:7px; padding:14px 16px; margin-top:15px;
  direction:__DIR__; text-align:__ALIGN__; line-height:1.75;
}
@media (max-width:600px) {
  .kpi-grid {grid-template-columns:1fr 1fr; gap:10px}
  .kpi-card {padding:14px 11px; min-height:108px}
  .kpi-value {font-size:clamp(.98rem,3.55vw,1.4rem);letter-spacing:-.04em}
  .kpi-label {font-size:.8rem; margin-bottom:9px}
  .hero {padding:19px 17px}
}
@media (max-width:380px) {
  .kpi-grid {grid-template-columns:1fr}
  .kpi-value {font-size:1.45rem}
}
</style>
    """.replace("__DIR__", dir_attr).replace("__ALIGN__", align),
    unsafe_allow_html=True,
)

if not DB_FILE.is_file():
    st.error(T["missing_file"])
    st.info(T["missing_file_hint"])
    st.stop()


@st.cache_data(show_spinner=False)
def read_air_traffic():
    with sqlite3.connect(DB_FILE) as conn:
        data = pd.read_sql_query(
            "SELECT year, month, airport, flight_type, direction, "
            "flights, passengers, time_granularity, source_file "
            "FROM air_traffic",
            conn,
        )
    data["month_num"] = data["month"].map(
        {month: index for index, month in enumerate(MONTHS_EN, start=1)}
    )
    for column in ("year", "passengers", "flights"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


try:
    data = read_air_traffic()
except (sqlite3.Error, ValueError, KeyError) as error:
    st.error(f"{T['load_error']} {error}")
    st.stop()

with st.sidebar:
    st.markdown("### ✈️ تحليلات الطيران" if RTL else "### ✈️ Aviation Hub")
    page = st.radio(
        T["navigation"],
        ["national", "airports", "monthly", "quality"],
        format_func=lambda key: T[key],
        key="dashboard_page",
    )
    st.divider()
    st.markdown(f"#### {T['filters']}")
    selected_airports = st.multiselect(
        T["airport_filter"],
        sorted(data.airport.dropna().unique()),
        format_func=lambda code: f"{airport_label(code)} ({code})",
        placeholder=T["all_airports"],
    )
    selected_types = st.multiselect(
        T["type_filter"],
        ["Domestic", "International"],
        default=["Domestic", "International"],
        format_func=lambda value: T["domestic"] if value == "Domestic" else T["international"],
    )
    selected_directions = st.multiselect(
        T["direction_filter"],
        ["ARRIVAL", "DEPARTURE"],
        default=["ARRIVAL", "DEPARTURE"],
        format_func=lambda value: T["arrival"] if value == "ARRIVAL" else T["departure"],
    )
    st.caption(T["source"])
    st.markdown(
        f'[{T["official_source_link"]}](https://www.gaca.gov.sa/ar/Open-Data/OpenDataLibrary)'
    )

st.markdown(
    f'<div class="hero"><h1>✈️ {T["title"]}</h1>'
    f'<p>{T["subtitle"]}</p></div>',
    unsafe_allow_html=True,
)

filtered = data[
    data.flight_type.isin(selected_types) &
    data.direction.isin(selected_directions)
].copy()
if selected_airports:
    filtered = filtered[filtered.airport.isin(selected_airports)]
if filtered.empty:
    st.warning(T["no_results"])
    st.stop()

if page == "national":
    st.subheader(T["national_title"])
    yearly = (
        filtered.groupby("year", as_index=False)
        .agg(
            passengers=("passengers", "sum"),
            flights=("flights", "sum"),
            airports=("airport", "nunique"),
        )
        .sort_values("year")
    )
    years = sorted(yearly.year.dropna().astype(int).tolist())
    selected_year = st.select_slider(
        T["indicator_year"], options=years, value=years[-1]
    )
    current = yearly[yearly.year == selected_year].iloc[0]
    render_kpis([
        (T["passengers"], number(current.passengers)),
        (T["movements"], number(current.flights)),
        (T["airports_count"], number(current.airports)),
        (
            T["passengers_per_movement"],
            number(current.passengers / current.flights, 2)
            if current.flights else "—",
        ),
    ])

    # Year-over-year comparison only for airports with monthly records
    # in all 12 months of both comparison years.
    if selected_year == 2025:
        complete_coverage = (
            data[data.year.isin([2024, 2025]) & data.month_num.notna()]
            .groupby(["airport", "year"]).month_num.nunique()
            .unstack(fill_value=0)
            .reindex(columns=[2024, 2025], fill_value=0)
        )
        complete_codes = complete_coverage.index[
            (complete_coverage[2024] == 12) &
            (complete_coverage[2025] == 12)
        ]
        comparable = filtered[
            filtered.airport.isin(complete_codes) &
            filtered.year.isin([2024, 2025])
        ]
        comparison_totals = comparable.groupby("year")[["passengers", "flights"]].sum()
        if (
            {2024, 2025}.issubset(comparison_totals.index)
            and comparison_totals.loc[2024, "passengers"] > 0
            and comparison_totals.loc[2024, "flights"] > 0
        ):
            passenger_change = (
                (comparison_totals.loc[2025, "passengers"] /
                 comparison_totals.loc[2024, "passengers"] - 1) * 100
            )
            movement_change = (
                (comparison_totals.loc[2025, "flights"] /
                 comparison_totals.loc[2024, "flights"] - 1) * 100
            )
            st.markdown(f"#### {T['national_growth_title']}")
            render_kpis([
                (T["passenger_yoy_kpi"], f"{passenger_change:+.2f}%"),
                (T["movement_yoy_kpi"], f"{movement_change:+.2f}%"),
            ])
            st.caption(
                T["national_growth_note"].format(
                    airports=int(comparable.airport.nunique())
                )
            )

    left, right = st.columns(2)
    with left:
        st.markdown(f"#### {T['passenger_trend']}")
        plot = px.line(
            yearly, x="year", y="passengers", markers=True,
            labels={"year": T["year"], "passengers": T["passengers"]},
            color_discrete_sequence=PALETTE,
        )
        figure(plot)
    with right:
        st.markdown(f"#### {T['movement_trend']}")
        plot = px.bar(
            yearly, x="year", y="flights",
            labels={"year": T["year"], "flights": T["movements"]},
            color_discrete_sequence=[PALETTE[1]],
        )
        figure(plot)

    st.markdown(f"#### {T['type_comparison_title']}")
    by_type = (
        filtered[filtered.year == selected_year]
        .groupby("flight_type", as_index=False)
        .passengers.sum()
    )
    by_type[T["type_filter"]] = by_type.flight_type.map({
        "Domestic": T["domestic"], "International": T["international"]
    })
    type_plot = px.bar(
        by_type,
        x=T["type_filter"], y="passengers",
        text="passengers",
        color=T["type_filter"],
        color_discrete_sequence=PALETTE,
        labels={"passengers": T["passengers"], T["type_filter"]: T["type_filter"]},
    )
    type_plot.update_traces(
        texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False
    )
    type_plot.update_layout(showlegend=False)
    figure(type_plot, height=340)

    yearly[T["passenger_growth"]] = (
        yearly.passengers.pct_change() * 100
    ).round(2)
    yearly[T["movement_growth"]] = (
        yearly.flights.pct_change() * 100
    ).round(2)
    table = yearly.rename(columns={
        "year": T["year"],
        "passengers": T["passengers"],
        "flights": T["movements"],
        "airports": T["airports_count"],
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    info_note(T["annual_note"])

elif page == "airports":
    st.subheader(T["airport_title"])
    selected_year = st.selectbox(
        T["indicator_year"],
        sorted(filtered.year.dropna().astype(int).unique(), reverse=True),
    )
    ranking = (
        filtered[filtered.year == selected_year]
        .groupby("airport", as_index=False)
        .agg(passengers=("passengers", "sum"), flights=("flights", "sum"))
        .sort_values("passengers", ascending=False)
    )
    ranking["airport_name"] = ranking.airport.map(airport_label)
    total_passengers = ranking.passengers.sum()
    ranking["share_pct"] = (
        ranking.passengers / total_passengers * 100
        if total_passengers else 0
    ).round(2)
    if len(ranking) < 2:
        # Streamlit sliders require min_value < max_value.
        # A single airport may still be inspected in the table below.
        st.info(T["select_two_airports"])
        st.caption(T["one_airport_note"])
    else:
        count = st.slider(
            T["show_count"], min_value=2,
            max_value=len(ranking), value=min(10, len(ranking)),
        )
        plot = px.bar(
            ranking.head(count).iloc[::-1],
            x="passengers", y="airport_name", orientation="h",
            color_discrete_sequence=[PALETTE[0]],
            hover_data={"share_pct": True},
            text="share_pct",
            labels={
                "passengers": T["passengers"],
                "airport_name": T["airport_name"],
                "share_pct": T["share_pct"],
            },
        )
        plot.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside",
            cliponaxis=False,
        )
        plot.update_layout(margin=dict(t=45, b=35, l=110, r=70))
        figure(plot, max(380, count * 37))
    ranking_table = ranking.rename(columns={
        "airport": "IATA",
        "airport_name": T["airport_name"],
        "passengers": T["passengers"],
        "flights": T["movements"],
        "share_pct": T["share_pct"],
    })
    st.dataframe(ranking_table, use_container_width=True, hide_index=True)
    st.download_button(
        T["download_ranking"],
        ranking_table.to_csv(index=False).encode("utf-8-sig"),
        "airports_ranking.csv", mime="text/csv",
    )
    st.divider()
    st.subheader(T["airport_comparison"])
    full_years = st.checkbox(T["twelve_months"], value=True)

    comparison = filtered[filtered.year.isin([2024, 2025])].copy()
    if full_years:
        coverage = (
            data[data.year.isin([2024, 2025]) & data.month_num.notna()]
            .groupby(["airport", "year"]).month_num.nunique()
            .unstack(fill_value=0)
            .reindex(columns=[2024, 2025], fill_value=0)
        )
        complete_airports = coverage[
            (coverage[2024] == 12) & (coverage[2025] == 12)
        ].index
        comparison = comparison[comparison.airport.isin(complete_airports)]

    grouped = (
        comparison.groupby(["airport", "year"], as_index=False)
        .passengers.sum()
    )
    pivot = (
        grouped.pivot_table(
            index="airport", columns="year",
            values="passengers", fill_value=0
        )
        .reindex(columns=[2024, 2025], fill_value=0)
        .reset_index()
    ) if not grouped.empty else pd.DataFrame()

    if pivot.empty:
        st.info(T["insufficient_comparison"])
    else:
        pivot[T["airport_name"]] = pivot.airport.map(airport_label)
        pivot[T["passenger_diff"]] = pivot[2025] - pivot[2024]
        pivot[T["growth_pct"]] = (
            pivot[T["passenger_diff"]] /
            pivot[2024].replace(0, float("nan")) * 100
        ).round(2)
        comparison_table = (
            pivot.rename(columns={
                "airport": "IATA",
                2024: T["passengers_2024"],
                2025: T["passengers_2025"],
            })
            [["IATA", T["airport_name"], T["passengers_2024"],
              T["passengers_2025"], T["passenger_diff"], T["growth_pct"]]]
            .sort_values(T["passenger_diff"], ascending=False)
        )
        st.dataframe(
            comparison_table, hide_index=True, use_container_width=True
        )
        st.download_button(
            T["download_comparison"],
            comparison_table.to_csv(index=False).encode("utf-8-sig"),
            "airport_growth_2024_2025.csv", mime="text/csv",
        )
    info_note(T["airport_note"])

elif page == "monthly":
    st.subheader(T["monthly_title"])
    monthly_source = filtered[filtered.month_num.notna()].copy()
    available_years = sorted(
        monthly_source.year.dropna().astype(int).unique().tolist()
    )
    selected_years = st.multiselect(
        T["years_filter"], available_years,
        default=[year for year in (2024, 2025) if year in available_years],
    )
    metric = st.radio(
        T["metric_select"], ["passengers", "flights"],
        format_func=lambda key: T["passengers"] if key == "passengers" else T["movements"],
        horizontal=True,
    )
    if not selected_years:
        st.info(T["choose_year"])
        st.stop()
    grouped = (
        monthly_source[monthly_source.year.isin(selected_years)]
        .groupby(["year", "month_num"], as_index=False)[metric].sum()
        .sort_values(["year", "month_num"])
    )
    grouped["year_label"] = grouped.year.astype(int).astype(str)
    plot = px.line(
        grouped, x="month_num", y=metric, color="year_label",
        markers=True, color_discrete_sequence=PALETTE,
        labels={
            "month_num": T["month"],
            metric: T["passengers"] if metric == "passengers" else T["movements"],
            "year_label": T["year"],
        },
    )
    plot.update_xaxes(
        tickmode="array", tickvals=list(range(1, 13)),
        ticktext=MONTHS_AR if RTL else MONTHS_EN,
    )
    figure(plot, height=465)

    grouped[T["month"]] = grouped.month_num.astype(int).map(
        dict(enumerate(MONTHS_AR if RTL else MONTHS_EN, 1))
    )
    metric_label = T["passengers"] if metric == "passengers" else T["movements"]
    monthly_table = grouped.rename(columns={
        "year": T["year"], metric: metric_label,
    })[[T["year"], T["month"], metric_label]]
    st.dataframe(monthly_table, hide_index=True, use_container_width=True)
    st.download_button(
        T["download_monthly"],
        monthly_table.to_csv(index=False).encode("utf-8-sig"),
        "monthly_aviation.csv", mime="text/csv",
    )
    info_note(T["monthly_note"])

else:
    st.subheader(T["quality_title"])
    quality = (
        data.groupby("year", as_index=False)
        .agg(
            records=("year", "size"),
            airports=("airport", "nunique"),
            months=("month_num", "nunique"),
            missing_passengers=("passengers", lambda s: int(s.isna().sum())),
            missing_movements=("flights", lambda s: int(s.isna().sum())),
        )
    )
    quality[T["granularity"]] = quality.year.map(
        lambda year: T["annual_level"] if year == 2022 else T["monthly_level"]
    )
    quality_table = quality.rename(columns={
        "year": T["year"],
        "records": T["records"],
        "airports": T["coverage_airports"],
        "months": T["months_count"],
        "missing_passengers": T["missing_passengers"],
        "missing_movements": T["missing_movements"],
    })
    st.dataframe(quality_table, hide_index=True, use_container_width=True)
    st.markdown(f"#### {T['coverage_title']}")
    coverage = (
        data[data.year.isin([2024, 2025]) & data.month_num.notna()]
        .groupby(["airport", "year"]).month_num.nunique()
        .unstack(fill_value=0)
        .reindex(columns=[2024, 2025], fill_value=0)
        .reset_index()
    )
    coverage[T["airport_name"]] = coverage.airport.map(airport_label)
    coverage_table = coverage.rename(columns={
        "airport": "IATA",
        2024: T["months_2024"],
        2025: T["months_2025"],
    })[["IATA", T["airport_name"], T["months_2024"], T["months_2025"]]]
    st.dataframe(coverage_table, hide_index=True, use_container_width=True)
    info_note(T["quality_note"])
