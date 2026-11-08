import streamlit as st
import pandas as pd
from datetime import date, timedelta
from scanner import run_scan
from storage import load_watchlist, save_watchlist, load_catalysts
from data_sources import fetch_fda_approvals, fetch_clinical_trials
st.set_page_config(page_title="Biotech FDA Catalyst Intelligence", page_icon="🧬", layout="wide")
st.title("Biotech FDA Catalyst Intelligence")
st.caption("نسخة MVP مجانية — أداة بحث ومراقبة وليست توصية استثمارية.")

with st.sidebar:
    st.header("إعدادات الفحص")
    tickers_text = st.text_area("الأسهم المراد مراقبتها (Ticker لكل سطر)", value="\n".join(load_watchlist()))
    if st.button("حفظ قائمة المراقبة", use_container_width=True):
        save_watchlist([x.strip().upper() for x in tickers_text.splitlines() if x.strip()])
        st.success("تم حفظ قائمة المراقبة.")
    lookback = st.slider("الفترة التاريخية للأسعار (أيام)", 30, 365, 90, 15)
    run_button = st.button("تشغيل الفحص الآن", type="primary", use_container_width=True)

tabs = st.tabs(["الفرص والأسهم", "تقويم FDA", "التجارب السريرية", "منهجية ومخاطر"])

if run_button:
    tickers = [x.strip().upper() for x in tickers_text.splitlines() if x.strip()]
    with st.spinner("جمع البيانات وتحليل الأسهم... قد يستغرق ذلك بعض الوقت."):
        result = run_scan(tickers, lookback_days=lookback)
    st.session_state["scan"] = result

with tabs[0]:
    st.subheader("نتائج الماسح")
    if "scan" not in st.session_state:
        st.info("أدخل رموز الأسهم في القائمة الجانبية ثم اضغط «تشغيل الفحص الآن».")
    else:
        df = st.session_state["scan"]
        if df.empty:
            st.warning("لم تتوفر بيانات كافية. تحقق من الاتصال أو رموز الأسهم.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("عدد الأسهم", len(df))
            c2.metric("إشارات متابعة صاعدة", int((df["signal"] == "Bullish watch").sum()))
            c3.metric("إشارات متابعة هابطة", int((df["signal"] == "Bearish watch").sum()))
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("تنزيل النتائج CSV", df.to_csv(index=False).encode("utf-8-sig"),
                               file_name=f"biotech_scan_{date.today()}.csv", mime="text/csv")
            st.caption("الدرجات أولية وقائمة على قواعد شفافة؛ ليست احتمالات موافقة FDA ولا توقعات سعرية مؤكدة.")

with tabs[1]:
    st.subheader("موافقات FDA المنشورة حديثاً")
    st.caption("تعرض هذه القائمة سجلات موافقات دوائية منشورة في قاعدة Drugs@FDA، ولا تمثل تقويماً مستقبلياً لمواعيد PDUFA.")
    if st.button("تحديث بيانات الموافقات"):
        with st.spinner("جلب بيانات openFDA..."):
            approvals = fetch_fda_approvals(limit=100)
        st.session_state["approvals"] = approvals
    if "approvals" in st.session_state:
        st.dataframe(st.session_state["approvals"], use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("التجارب السريرية")
    q = st.text_input("ابحث عن مرض أو دواء أو شركة", value="biotechnology")
    if st.button("بحث في ClinicalTrials.gov"):
        with st.spinner("البحث في سجل التجارب..."):
            trials = fetch_clinical_trials(q, page_size=50)
        st.session_state["trials"] = trials
    if "trials" in st.session_state:
        st.dataframe(st.session_state["trials"], use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("ما الذي تفعله النسخة الأولى؟")
    st.markdown("""
- تجلب أسعاراً تاريخية ومؤشرات أساسية عبر Yahoo Finance بواسطة `yfinance`.
- تجلب بيانات مالية منشورة من SEC Company Facts عندما يتوفر CIK.
- تعرض سجلات موافقات FDA من openFDA.
- تبحث في ClinicalTrials.gov.
- تنتج مؤشرات متابعة أولية من الزخم والتذبذب والسيولة وتغير السعر.

**ما لا تدّعيه النسخة الأولى:** لا تستخرج تواريخ PDUFA موثوقة لكل الشركات تلقائياً، ولا تحسب احتمالية FDA علمية، ولا توفر بيانات خيارات أو إجماع EPS مدفوع/محدّث. هذه تحتاج مصادر إضافية أو إدخالاً موثقاً يدوياً.
    """)
    st.warning("أحداث FDA ثنائية وقد تسبب فجوات سعرية كبيرة. لا تعتمد على وقف الخسارة وحده عند الاحتفاظ بالسهم خلال القرار.")
