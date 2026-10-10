"""Saudi Aviation Analytics | لوحة تحليلات الطيران السعودي — bilingual Streamlit app."""
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Saudi Aviation Analytics | تحليلات الطيران السعودي", page_icon="✈️", layout="wide")

DB = Path(__file__).resolve().parent / "air_traffic.sqlite"
MONTH_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTH_AR = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
AIRPORT_NAMES = {
    "ABT": ("الباحة", "Al Baha"), "AHB": ("أبها", "Abha"),
    "AJF": ("الجوف", "Al Jouf"), "AQI": ("القيصومة", "Al Qaisumah"),
    "BHH": ("بيشة", "Bisha"), "DMM": ("الدمام", "Dammam"),
    "DWD": ("الدوادمي", "Dawadmi"), "EAM": ("نجران", "Najran"),
    "EJH": ("الوجه", "Al Wajh"), "ELQ": ("القصيم", "Qassim"),
    "GIZ": ("جازان", "Jazan"), "HAS": ("حائل", "Hail"),
    "HOF": ("الأحساء", "Al Ahsa"), "JED": ("جدة", "Jeddah"),
    "MED": ("المدينة المنورة", "Madinah"), "NUM": ("نيوم", "NEOM"),
    "RAE": ("عرعر", "Arar"), "RAH": ("رفحاء", "Rafha"),
    "RGB": ("رابغ", "Rabigh"), "RSI": ("البحر الأحمر", "Red Sea"),
    "RUH": ("الرياض", "Riyadh"), "SHW": ("شرورة", "Sharurah"),
    "TIF": ("الطائف", "Taif"), "TUI": ("طريف", "Turaif"),
    "TUU": ("تبوك", "Tabuk"), "ULH": ("العلا", "Al Ula"),
    "URY": ("القريات", "Qurayyat"), "WAE": ("وادي الدواسر", "Wadi Al Dawasir"),
    "YNB": ("ينبع", "Yanbu")
}
PALETTE = ["#2dd4bf", "#38bdf8", "#f59e0b", "#a78bfa", "#fb7185"]

TEXT = {
    "ar": {
        "language": "اللغة | Language",
        "menu": "القسم", "home": "النظرة الوطنية", "airports": "أداء المطارات",
        "monthly": "التحليل الشهري", "quality": "جودة البيانات",
        "filters": "تصفية البيانات", "airports_filter": "المطارات",
        "all_airports": "جميع المطارات", "flight_type": "نوع الرحلة",
        "direction": "اتجاه الرحلة", "domestic": "داخلية", "international": "دولية",
        "arrival": "وصول", "departure": "مغادرة",
        "title": "تحليلات الطيران السعودي", "subtitle": "لوحة تفاعلية لتحليل حركة الطيران في المملكة العربية السعودية خلال الفترة 2020–2025",
        "source": "المصدر: ملفات الحركة الجوية المنشورة من الهيئة العامة للطيران المدني (2020–2025).",
        "no_data": "لا توجد بيانات مطابقة للفلاتر المحددة.",
        "missing_db": "ملف قاعدة البيانات air_traffic.sqlite غير موجود في المستودع.",
        "missing_db_help": "ارفعيه إلى جذر مستودع GitHub بجانب app.py، ثم أعيدي تشغيل التطبيق.",
        "home_header": "مؤشرات الحركة الجوية", "year_selector": "سنة المؤشرات",
        "passengers": "المسافرون", "flights": "حركات الطيران", "airport_count": "عدد المطارات",
        "per_flight": "مسافر لكل حركة", "trend_passengers": "تطور أعداد المسافرين",
        "trend_flights": "تطور حركات الطيران", "year": "السنة",
        "passengers_growth": "نمو المسافرين (%)", "flights_growth": "نمو حركات الطيران (%)",
        "annual_note": "ملاحظة منهجية: بيانات 2022 مجمعة سنويًا، بينما السنوات الأخرى تتضمن تفاصيل شهرية. تختلف تغطية المطارات بين السنوات؛ لذلك تعتبر المقارنات استكشافية حتى التحقق من اتساق نطاق الملفات.",
        "airport_header": "ترتيب المطارات", "show_airports": "عدد المطارات المعروضة",
        "share": "الحصة من المسافرين (%)", "airport": "المطار",
        "download_rank": "تحميل ترتيب المطارات CSV",
        "comparison": "مقارنة المطارات: 2024 و2025",
        "complete_months": "عرض المطارات ذات الأشهر الـ12 المسجلة في كلتا السنتين فقط",
        "p_2024": "المسافرون 2024", "p_2025": "المسافرون 2025",
        "change": "التغير في المسافرين", "growth": "معدل النمو (%)",
        "download_comparison": "تحميل مقارنة المطارات CSV",
        "missing_comparison": "لا تتوفر بيانات كافية للمقارنة وفق الفلاتر المختارة.",
        "comparison_note": "وجود سجلات للأشهر الاثني عشر لا يضمن اكتمال جميع أنواع الرحلات والاتجاهات. لا تُفسَّر الفروقات كأداء تشغيلي نهائي دون تدقيق نطاق التغطية.",
        "monthly_header": "اتجاهات الحركة الشهرية", "years_select": "سنوات العرض",
        "metric": "المؤشر", "select_year": "اختاري سنة واحدة على الأقل.",
        "month": "الشهر", "download_monthly": "تحميل البيانات الشهرية CSV",
        "monthly_note": "عام 2022 غير معروض هنا لأنه يتضمن مجاميع سنوية لا تفاصيل شهرية. سنتان وحدهما لا تثبتان نمطًا موسميًا مستقرًا.",
        "quality_header": "مراجعة جودة وتغطية البيانات",
        "records": "عدد السجلات", "airports_n": "المطارات",
        "months_n": "الأشهر المسجلة", "missing_passengers": "قيم المسافرين المفقودة",
        "missing_flights": "قيم الرحلات المفقودة", "granularity": "مستوى التفاصيل",
        "annual": "سنوي", "monthly_level": "شهري",
        "coverage": "الأشهر المسجلة لكل مطار",
        "months_2024": "أشهر 2024", "months_2025": "أشهر 2025",
        "quality_note": "غياب شهر من السجلات لا يعني بالضرورة توقف العمليات، كما أن توافر الأشهر لا يعني اكتمال كل فئة تشغيلية.",
        "source_file": "الملف الأصلي", "year_records": "ملخص السجلات حسب السنة",
    },
    "en": {
        "language": "Language | اللغة",
        "menu": "Section", "home": "National overview", "airports": "Airport performance",
        "monthly": "Monthly trends", "quality": "Data quality",
        "filters": "Data filters", "airports_filter": "Airports",
        "all_airports": "All airports", "flight_type": "Flight type",
        "direction": "Movement direction", "domestic": "Domestic", "international": "International",
        "arrival": "Arrival", "departure": "Departure",
        "title": "Saudi Aviation Analytics", "subtitle": "Interactive air-traffic analytics for Saudi Arabia, 2020–2025",
        "source": "Source: General Authority of Civil Aviation (GACA) publicly available air-traffic files, 2020–2025.",
        "no_data": "No data matches the current filters.",
        "missing_db": "Database file air_traffic.sqlite is missing from the repository.",
        "missing_db_help": "Upload it next to app.py at the GitHub repository root, then restart the app.",
        "home_header": "National air-traffic indicators", "year_selector": "Indicator year",
        "passengers": "Passengers", "flights": "Flight movements", "airport_count": "Airports",
        "per_flight": "Passengers per movement", "trend_passengers": "Passenger trends",
        "trend_flights": "Flight movement trends", "year": "Year",
        "passengers_growth": "Passenger growth (%)", "flights_growth": "Flight movements growth (%)",
        "annual_note": "Methodology: 2022 data is annual, while other years include monthly detail. Airport coverage differs between years, so cross-year comparisons remain exploratory until source scopes are validated.",
        "airport_header": "Airport rankings", "show_airports": "Airports to display",
        "share": "Passenger share (%)", "airport": "Airport",
        "download_rank": "Download airport rankings CSV",
        "comparison": "Airport comparison: 2024 vs 2025",
        "complete_months": "Include only airports with records for all 12 months in both years",
        "p_2024": "Passengers 2024", "p_2025": "Passengers 2025",
        "change": "Passenger change", "growth": "Growth rate (%)",
        "download_comparison": "Download airport comparison CSV",
        "missing_comparison": "Not enough data to compare with the selected filters.",
        "comparison_note": "Having records for all 12 months does not guarantee coverage of every flight type or direction. Treat the comparisons as preliminary pending scope checks.",
        "monthly_header": "Monthly air-traffic trends", "years_select": "Years to display",
        "metric": "Metric", "select_year": "Select at least one year.",
        "month": "Month", "download_monthly": "Download monthly data CSV",
        "monthly_note": "2022 is excluded from monthly charts because its data is annual. Two years alone do not establish a stable seasonal pattern.",
        "quality_header": "Data quality and coverage",
        "records": "Records", "airports_n": "Airports", "months_n": "Months represented",
        "missing_passengers": "Missing passenger values", "missing_flights": "Missing flight values",
        "granularity": "Granularity", "annual": "Annual", "monthly_level": "Monthly",
        "coverage": "Monthly coverage by airport", "months_2024": "Months 2024", "months_2025": "Months 2025",
        "quality_note": "Missing monthly records do not necessarily mean no traffic, and recorded months do not guarantee coverage of all operational categories.",
        "source_file": "Source file", "year_records": "Yearly record summary",
    }
}

with st.sidebar:
    language_choice = st.radio("اللغة | Language", ["العربية", "English"], horizontal=True, index=0)
lang = "ar" if language_choice == "العربية" else "en"
T = TEXT[lang]
rtl = lang == "ar"
direction_css = "rtl" if rtl else "ltr"
alignment_css = "right" if rtl else "left"

st.markdown(f"""
<style>
.stApp {{background:#0c1628;color:#edf7ff}}
[data-testid="stSidebar"] {{background:#122139}}
[data-testid="stMetric"] {{background:#162a44;border:1px solid #314863;border-radius:14px;padding:16px}}
[data-testid="stAppViewContainer"] .block-container {{
    padding-top:1.4rem; direction:{direction_css}; text-align:{alignment_css};
}}
[data-testid="stSidebar"] {{direction:{direction_css};text-align:{alignment_css};}}
h1,h2,h3 {{letter-spacing:-.01em}}
.hero {{background:linear-gradient(115deg,#133b52,#18304a 65%,#1a2341);
 border:1px solid #35546a;border-radius:22px;padding:24px 27px;margin:6px 0 24px;
 direction:{direction_css};text-align:{alignment_css};}}
.hero h1 {{margin:0;color:#f2faff;font-size:2rem}}
.hero p {{margin:7px 0 0;color:#b6d8e8}}
.note {{background:#182e49;border-inline-start:3px solid #38bdf8;
 padding:13px 15px;border-radius:7px;direction:{direction_css};text-align:{alignment_css};}}
</style>
""", unsafe_allow_html=True)

def name_of(code):
    pair = AIRPORT_NAMES.get(code)
    if pair is None:
        return code
    return pair[0] if rtl else pair[1]

def pretty_int(n):
    return f"{n:,.0f}" if pd.notna(n) else "—"

def plot(fig, height=410):
    fig.update_layout(template="plotly_dark", height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color="#deeaf5"), margin=dict(t=35,b=25,l=12,r=12),
        legend=dict(orientation="h", y=1.14))
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data(show_spinner=False)
def load_data():
    with sqlite3.connect(DB) as connection:
        frame = pd.read_sql_query(
            "SELECT year, month, airport, flight_type, direction, flights, passengers, time_granularity, source_file FROM air_traffic",
            connection)
    frame["month_num"] = frame["month"].map({m: i+1 for i,m in enumerate(MONTH_EN)})
    for field in ("year", "flights", "passengers"):
        frame[field] = pd.to_numeric(frame[field], errors="coerce")
    frame["year"] = frame["year"].astype("Int64")
    return frame

if not DB.is_file():
    st.error(T["missing_db"])
    st.info(T["missing_db_help"])
    st.stop()

try:
    df = load_data()
except Exception as exc:
    st.error(f"{T['missing_db']}: {exc}")
    st.stop()

with st.sidebar:
    st.markdown("### ✈️ Aviation Hub")
    section = st.radio(T["menu"], ["home", "airports", "monthly", "quality"],
        format_func=lambda x: T[x], index=0)
    st.divider()
    st.markdown(f"#### {T['filters']}")
    airports = sorted(df["airport"].dropna().unique().tolist())
    chosen_airports = st.multiselect(T["airports_filter"], airports,
        format_func=lambda x:f"{name_of(x)} ({x})", placeholder=T["all_airports"])
    chosen_types = st.multiselect(T["flight_type"], ["Domestic", "International"],
        default=["Domestic", "International"],
        format_func=lambda x: T["domestic"] if x=="Domestic" else T["international"])
    chosen_directions = st.multiselect(T["direction"], ["ARRIVAL", "DEPARTURE"],
        default=["ARRIVAL", "DEPARTURE"],
        format_func=lambda x: T["arrival"] if x=="ARRIVAL" else T["departure"])
    st.caption(T["source"])

st.markdown(f"""
<div class="hero"><h1>✈️ {T['title']}</h1><p>{T['subtitle']}</p></div>
""", unsafe_allow_html=True)

filtered = df[
    df["flight_type"].isin(chosen_types) &
    df["direction"].isin(chosen_directions)
].copy()
if chosen_airports:
    filtered = filtered[filtered["airport"].isin(chosen_airports)]
if filtered.empty:
    st.warning(T["no_data"])
    st.stop()

if section == "home":
    st.subheader(T["home_header"])
    yearly = (filtered.groupby("year", as_index=False)
        .agg(passengers=("passengers","sum"),flights=("flights","sum"),
             airports=("airport","nunique")).sort_values("year"))
    selected_year = st.select_slider(T["year_selector"],
        options=[int(x) for x in yearly.year.tolist()], value=int(yearly.year.max()))
    chosen = yearly[yearly.year==selected_year].iloc[0]
    a,b,c,d = st.columns(4)
    a.metric(T["passengers"], pretty_int(chosen.passengers))
    b.metric(T["flights"], pretty_int(chosen.flights))
    c.metric(T["airport_count"], int(chosen.airports))
    d.metric(T["per_flight"],
        f"{chosen.passengers/chosen.flights:,.2f}" if chosen.flights else "—")
    left,right=st.columns(2)
    with left:
        st.markdown(f"#### {T['trend_passengers']}")
        fig=px.line(yearly,x="year",y="passengers",markers=True,
                    labels={"year":T["year"],"passengers":T["passengers"]},
                    color_discrete_sequence=PALETTE)
        plot(fig)
    with right:
        st.markdown(f"#### {T['trend_flights']}")
        fig=px.bar(yearly,x="year",y="flights",
                   labels={"year":T["year"],"flights":T["flights"]},
                   color_discrete_sequence=[PALETTE[1]])
        plot(fig)
    yearly[T["passengers_growth"]] = (yearly.passengers.pct_change()*100).round(2)
    yearly[T["flights_growth"]] = (yearly.flights.pct_change()*100).round(2)
    st.dataframe(yearly.rename(columns={"year":T["year"],"passengers":T["passengers"],
        "flights":T["flights"],"airports":T["airport_count"]}),
        hide_index=True,use_container_width=True)
    st.markdown(f'<div class="note">{T["annual_note"]}</div>',unsafe_allow_html=True)

elif section == "airports":
    st.subheader(T["airport_header"])
    year = st.selectbox(T["year_selector"],
        sorted([int(y) for y in filtered.year.dropna().unique()],reverse=True))
    ranked=(filtered[filtered.year==year].groupby("airport",as_index=False)
       .agg(passengers=("passengers","sum"), flights=("flights","sum"))
       .sort_values("passengers",ascending=False))
    ranked["airport_name"] = ranked.airport.map(name_of)
    ranked["share_pct"] = (100*ranked.passengers/ranked.passengers.sum()).round(2)
    how_many=st.slider(T["show_airports"],1,len(ranked),min(10,len(ranked)))
    display=ranked.head(how_many).iloc[::-1]
    fig=px.bar(display,x="passengers",y="airport_name",orientation="h",
        hover_data={"share_pct":True},color_discrete_sequence=[PALETTE[0]],
        labels={"passengers":T["passengers"],"airport_name":T["airport"],
                "share_pct":T["share"]})
    plot(fig,max(380,how_many*37))
    rank_display=ranked.rename(columns={"airport": "IATA", "airport_name":T["airport"],
        "passengers":T["passengers"],"flights":T["flights"],"share_pct":T["share"]})
    st.dataframe(rank_display,hide_index=True,use_container_width=True)
    st.download_button(T["download_rank"],
        rank_display.to_csv(index=False).encode("utf-8-sig"),"airport_rankings.csv","text/csv")
    st.divider()
    st.subheader(T["comparison"])
    complete=st.checkbox(T["complete_months"],value=True)
    compare=filtered[filtered.year.isin([2024,2025])].copy()
    if complete:
        coverage=(df[df.year.isin([2024,2025]) & df.month_num.notna()]
              .groupby(["airport","year"]).month_num.nunique()
              .unstack(fill_value=0).reindex(columns=[2024,2025],fill_value=0))
        valid=coverage[(coverage[2024]==12)&(coverage[2025]==12)].index
        compare=compare[compare.airport.isin(valid)]
    table=compare.groupby(["airport","year"],as_index=False).passengers.sum()
    pivot=(table.pivot_table(index="airport",columns="year",values="passengers",fill_value=0)
           .reindex(columns=[2024,2025],fill_value=0).reset_index())
    if not pivot.empty and 2024 in pivot.columns and 2025 in pivot.columns:
        pivot[T["airport"]]=pivot.airport.map(name_of)
        pivot[T["change"]]=pivot[2025]-pivot[2024]
        pivot[T["growth"]]=(100*pivot[T["change"]]/pivot[2024].replace(0,float("nan"))).round(2)
        result=pivot.rename(columns={"airport":"IATA",2024:T["p_2024"],2025:T["p_2025"]})
        result=result[["IATA",T["airport"],T["p_2024"],T["p_2025"],T["change"],T["growth"]]]
        result=result.sort_values(T["change"],ascending=False)
        st.dataframe(result,hide_index=True,use_container_width=True)
        st.download_button(T["download_comparison"],
            result.to_csv(index=False).encode("utf-8-sig"),"airport_growth_2024_2025.csv","text/csv")
    else:
        st.info(T["missing_comparison"])
    st.markdown(f'<div class="note">{T["comparison_note"]}</div>',unsafe_allow_html=True)

elif section == "monthly":
    st.subheader(T["monthly_header"])
    monthly=filtered[filtered.month_num.notna()].copy()
    available=sorted([int(y) for y in monthly.year.dropna().unique()])
    selected_years=st.multiselect(T["years_select"],available,
        default=[x for x in [2024,2025] if x in available])
    metric=st.radio(T["metric"],["passengers","flights"],horizontal=True,
        format_func=lambda x:T["passengers"] if x=="passengers" else T["flights"])
    if not selected_years:
        st.info(T["select_year"])
        st.stop()
    monthly=(monthly[monthly.year.isin(selected_years)]
             .groupby(["year","month_num"],as_index=False)[metric].sum()
             .sort_values(["year","month_num"]))
    monthly["year_label"]=monthly.year.astype(str)
    fig=px.line(monthly,x="month_num",y=metric,color="year_label",markers=True,
        labels={"month_num":T["month"],metric:T[metric],"year_label":T["year"]},
        color_discrete_sequence=PALETTE)
    fig.update_xaxes(tickmode="array",tickvals=list(range(1,13)),
        ticktext=MONTH_AR if rtl else MONTH_EN)
    plot(fig,490)
    monthly[T["month"]]=monthly.month_num.astype(int).map(
        {i+1:m for i,m in enumerate(MONTH_AR if rtl else MONTH_EN)})
    printable=monthly.rename(columns={"year":T["year"],metric:T[metric]})
    st.dataframe(printable[[T["year"],T["month"],T[metric]]],
        hide_index=True,use_container_width=True)
    st.download_button(T["download_monthly"],
        printable[[T["year"],T["month"],T[metric]]].to_csv(index=False).encode("utf-8-sig"),
        "monthly_aviation.csv","text/csv")
    st.markdown(f'<div class="note">{T["monthly_note"]}</div>',unsafe_allow_html=True)

else:
    st.subheader(T["quality_header"])
    byyear=(df.groupby("year",as_index=False)
       .agg(records=("year","size"), airports=("airport","nunique"),
            months=("month_num","nunique"),
            missing_passengers=("passengers",lambda s:int(s.isna().sum())),
            missing_flights=("flights",lambda s:int(s.isna().sum()))))
    byyear[T["granularity"]]=byyear.year.apply(
        lambda y:T["annual"] if y==2022 else T["monthly_level"])
    st.markdown(f"#### {T['year_records']}")
    quality_display=byyear.rename(columns={
        "year":T["year"],"records":T["records"],"airports":T["airports_n"],
        "months":T["months_n"],"missing_passengers":T["missing_passengers"],
        "missing_flights":T["missing_flights"]})
    st.dataframe(quality_display,hide_index=True,use_container_width=True)
    st.markdown(f"#### {T['coverage']}")
    coverage=(df[df.year.isin([2024,2025]) & df.month_num.notna()]
        .groupby(["airport","year"]).month_num.nunique().unstack(fill_value=0)
        .reindex(columns=[2024,2025],fill_value=0).reset_index())
    coverage[T["airport"]]=coverage.airport.map(name_of)
    coverage=coverage.rename(columns={"airport":"IATA",2024:T["months_2024"],2025:T["months_2025"]})
    st.dataframe(coverage[["IATA",T["airport"],T["months_2024"],T["months_2025"]]],
        hide_index=True,use_container_width=True)
    st.markdown(f'<div class="note">{T["quality_note"]}</div>',unsafe_allow_html=True)
