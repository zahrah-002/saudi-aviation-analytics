"""Saudi Aviation Analytics — Streamlit dashboard for public Saudi air-traffic data."""
from pathlib import Path
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Saudi Aviation Analytics", page_icon="✈️", layout="wide")
DB = Path(__file__).resolve().parent / "air_traffic.sqlite"
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
MONTH_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
AIRPORTS = {
    "ABT":"الباحة","AHB":"أبها","AJF":"الجوف","AQI":"القيصومة",
    "BHH":"بيشة","DMM":"الدمام","DWD":"الدوادمي","EAM":"نجران",
    "EJH":"الوجه","ELQ":"القصيم","GIZ":"جازان","HAS":"حائل",
    "HOF":"الأحساء","JED":"جدة","MED":"المدينة المنورة","NUM":"نيوم",
    "RAE":"عرعر","RAH":"رفحاء","RGB":"رابغ","RSI":"البحر الأحمر",
    "RUH":"الرياض","SHW":"شرورة","TIF":"الطائف","TUI":"طريف",
    "TUU":"تبوك","ULH":"العلا","URY":"القريات","WAE":"وادي الدواسر",
    "YNB":"ينبع"
}
PALETTE = ["#2dd4bf","#38bdf8","#f59e0b","#a78bfa","#fb7185"]
st.markdown("""
<style>
.stApp{background:#0c1628;color:#edf7ff}
[data-testid="stSidebar"]{background:#122139}
[data-testid="stMetric"]{background:#162a44;border:1px solid #314863;border-radius:14px;padding:17px}
h1,h2,h3{letter-spacing:-.01em}
.block-container{padding-top:1.5rem}
.hero{background:linear-gradient(115deg,#133b52,#18304a 65%,#1a2341);border:1px solid #35546a;border-radius:22px;padding:24px 27px;margin:6px 0 24px}
.hero h1{margin:0;color:#f2faff;font-size:2rem}
.hero p{margin:7px 0 0;color:#b6d8e8}
.note{background:#182e49;border-left:3px solid #38bdf8;padding:13px 15px;border-radius:7px}
</style>
""",unsafe_allow_html=True)

if not DB.is_file():
    st.error("لم يُرفع ملف البيانات بعد: air_traffic.sqlite")
    st.info("ارفعي الملف في جذر مستودع GitHub بجانب app.py، ثم أعيدي تشغيل التطبيق.")
    st.stop()

@st.cache_data(show_spinner="جاري تحميل بيانات الطيران...")
def load_data():
    with sqlite3.connect(DB) as conn:
        d = pd.read_sql_query(
            "SELECT year,month,airport,flight_type,direction,flights,passengers,time_granularity,source_file FROM air_traffic",conn
        )
    d["month_num"] = d["month"].map({m:i+1 for i,m in enumerate(MONTHS)})
    d["airport_name"] = d["airport"].map(AIRPORTS).fillna(d["airport"])
    return d

def format_int(n):
    return f"{n:,.0f}" if pd.notna(n) else "—"

def chart(fig, height=410):
    fig.update_layout(template="plotly_dark", height=height,
       paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
       font=dict(family="Arial",color="#deeaf5"),
       margin=dict(t=35,b=25,l=10,r=10),
       legend=dict(orientation="h",y=1.13))
    st.plotly_chart(fig,use_container_width=True)

data=load_data()
with st.sidebar:
    st.title("✈️ Aviation Hub")
    page=st.radio("القسم",["🏠 النظرة الوطنية","🛬 المطارات","📆 الحركة الشهرية","🧪 جودة البيانات"])
    st.divider()
    selected_airports=st.multiselect("المطارات",sorted(data.airport.dropna().unique()),
       format_func=lambda x:f"{AIRPORTS.get(x,x)} ({x})",placeholder="جميع المطارات")
    types=st.multiselect("نوع الرحلة",["Domestic","International"],
       default=["Domestic","International"],
       format_func=lambda x:"داخلية" if x=="Domestic" else "دولية")
    directions=st.multiselect("الاتجاه",["ARRIVAL","DEPARTURE"],
       default=["ARRIVAL","DEPARTURE"],
       format_func=lambda x:"وصول" if x=="ARRIVAL" else "مغادرة")
    st.caption("المصدر: ملفات الهيئة العامة للطيران المدني 2020–2025. البيانات المجمعة تتطلب تدقيق التغطية عند مقارنة السنوات.")

d=data[data.flight_type.isin(types)&data.direction.isin(directions)].copy()
if selected_airports: d=d[d.airport.isin(selected_airports)]
st.markdown("""<div class="hero" dir="rtl"><h1>تحليلات الطيران السعودي | Saudi Aviation</h1><p>لوحة تفاعلية تجمع SQL وPython وStreamlit لاستكشاف الحركة الجوية في المملكة، 2020–2025</p></div>""",unsafe_allow_html=True)
if d.empty:
    st.warning("لا توجد نتائج مطابقة للفلاتر الحالية.")
    st.stop()

if page=="🏠 النظرة الوطنية":
    st.subheader("المؤشرات الوطنية | National Overview")
    yearly=d.groupby("year",as_index=False).agg(passengers=("passengers","sum"),
        flights=("flights","sum"),airports=("airport","nunique")).sort_values("year")
    yy=st.select_slider("سنة المؤشرات",options=yearly.year.tolist(),value=int(yearly.year.max()))
    r=yearly[yearly.year==yy].iloc[0]
    a,b,c,e=st.columns(4)
    a.metric("المسافرون",format_int(r.passengers))
    b.metric("حركات الطيران",format_int(r.flights))
    c.metric("عدد المطارات",int(r.airports))
    e.metric("مسافر لكل حركة",f"{r.passengers/r.flights:,.2f}" if r.flights else "—")
    x,y=st.columns(2)
    with x:
        st.markdown("#### تطور أعداد المسافرين")
        fig=px.line(yearly,x="year",y="passengers",markers=True,color_discrete_sequence=PALETTE)
        chart(fig)
    with y:
        st.markdown("#### حركات الطيران")
        fig=px.bar(yearly,x="year",y="flights",color_discrete_sequence=[PALETTE[1]])
        chart(fig)
    yearly["passenger_growth_pct"]=(yearly.passengers.pct_change()*100).round(2)
    yearly["flight_growth_pct"]=(yearly.flights.pct_change()*100).round(2)
    st.dataframe(yearly,use_container_width=True,hide_index=True)
    st.markdown('<div class="note" dir="rtl">تنبيه منهجي: بيانات 2022 سنوية المستوى، بينما تتوفر تفاصيل شهرية في السنوات الأخرى. كما تختلف تغطية المطارات؛ لذلك معدلات النمو استكشافية حتى التحقق من اتساق تعريفات الملفات.</div>',unsafe_allow_html=True)

elif page=="🛬 المطارات":
    st.subheader("أداء المطارات | Airport Performance")
    yy=st.selectbox("السنة",sorted(d.year.unique(),reverse=True))
    ranked=d[d.year==yy].groupby(["airport","airport_name"],as_index=False).agg(
        passengers=("passengers","sum"),flights=("flights","sum")).sort_values("passengers",ascending=False)
    ranked["share_pct"]=(ranked.passengers/ranked.passengers.sum()*100).round(2)
    n=st.slider("المطارات المعروضة",1,len(ranked),min(10,len(ranked)))
    fig=px.bar(ranked.head(n).iloc[::-1],x="passengers",y="airport_name",orientation="h",
      color_discrete_sequence=[PALETTE[0]],hover_data=["share_pct"])
    chart(fig,max(370,n*32))
    st.dataframe(ranked,use_container_width=True,hide_index=True)
    st.download_button("تحميل ترتيب المطارات CSV",ranked.to_csv(index=False).encode("utf-8-sig"),
      "airports_ranking.csv","text/csv")
    st.divider()
    st.subheader("مقارنة 2024 و2025")
    coverage=data[data.year.isin([2024,2025]) & data.month_num.notna()].groupby(
        ["airport","year"]).month_num.nunique().unstack(fill_value=0)
    eligible=coverage[(coverage.get(2024,0)==12)&(coverage.get(2025,0)==12)].index
    full=st.checkbox("المطارات التي لها سجلات في 12 شهرًا لكل سنة فقط",value=True)
    pair=d[d.year.isin([2024,2025])].copy()
    if full: pair=pair[pair.airport.isin(eligible)]
    comp=pair.groupby(["airport","airport_name","year"],as_index=False).passengers.sum()
    comp=comp.pivot_table(index=["airport","airport_name"],columns="year",values="passengers",fill_value=0).reset_index()
    if 2024 in comp.columns and 2025 in comp.columns:
        comp["change"]=comp[2025]-comp[2024]
        comp["growth_pct"]=(comp["change"]/comp[2024].replace(0,float("nan"))*100).round(2)
        st.dataframe(comp.sort_values("change",ascending=False),hide_index=True,use_container_width=True)
        st.download_button("تحميل مقارنة السنوات CSV",comp.to_csv(index=False).encode("utf-8-sig"),
          "airport_growth_2024_2025.csv","text/csv")
    else: st.info("لا توجد بيانات كافية للمقارنة.")

elif page=="📆 الحركة الشهرية":
    st.subheader("التحليل الشهري | Monthly Trends")
    md=d[d.month_num.notna()]
    ys=st.multiselect("سنوات العرض",sorted(md.year.unique()),
      default=[y for y in [2024,2025] if y in md.year.unique()])
    metric=st.radio("المؤشر",["passengers","flights"],format_func=lambda x:"المسافرون" if x=="passengers" else "حركات الطيران",horizontal=True)
    if not ys: st.info("اختاري سنة.");st.stop()
    m=md[md.year.isin(ys)].groupby(["year","month_num"],as_index=False)[metric].sum()
    m["الشهر"]=m.month_num.astype(int).apply(lambda i:MONTH_AR[i-1])
    m["السنة"]=m.year.astype(str)
    fig=px.line(m,x="الشهر",y=metric,color="السنة",markers=True,
       category_orders={"الشهر":MONTH_AR},color_discrete_sequence=PALETTE)
    chart(fig,470)
    st.dataframe(m,hide_index=True,use_container_width=True)
    st.download_button("تحميل البيانات الشهرية CSV",m.to_csv(index=False).encode("utf-8-sig"),
      "monthly_aviation.csv","text/csv")
    st.caption("2022 لا تظهر في الرسوم الشهرية لأنها وردت بصيغة سنوية. وجود تغيرات خلال سنتين لا يثبت نمطًا موسميًا ثابتًا.")

else:
    st.subheader("جودة البيانات | Data Quality")
    quality=data.groupby("year",as_index=False).agg(
        records=("year","size"),airports=("airport","nunique"),
        months=("month_num","nunique"),missing_passengers=("passengers",lambda x:int(x.isna().sum())),
        missing_flights=("flights",lambda x:int(x.isna().sum())))
    quality["granularity"]=quality.year.apply(lambda y:"Annual" if y==2022 else "Monthly")
    st.dataframe(quality,hide_index=True,use_container_width=True)
    coverage=data[data.year.isin([2024,2025]) & data.month_num.notna()].groupby(
        ["airport","year"]).month_num.nunique().unstack(fill_value=0)
    coverage=coverage.rename(columns={2024:"months_2024",2025:"months_2025"}).reset_index()
    st.subheader("تغطية الأشهر حسب المطار")
    st.dataframe(coverage,hide_index=True,use_container_width=True)
    st.caption("غياب سجلات شهر لا يعني بالضرورة توقف الرحلات. اكتمال الأشهر لا يضمن وجود جميع أنواع الرحلات واتجاهاتها.")
