# dashboard.py – Ultimatives Live-Dashboard für den KI Trading Bot

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="KI Trading Bot Dashboard", layout="wide")

# =============================
# LAYOUT
# =============================
st.title("📊 KI Trading Bot Dashboard")
st.markdown("**Status:** Live | 24/7 Online | Mutation aktiviert 🧬")
st.divider()

# =============================
# KAPITALVERLAUF & STATS
# =============================
col1, col2, col3 = st.columns(3)

try:
    df_perf = pd.read_csv("performance_log.csv")
    col1.metric("📈 Kapital", f"{df_perf['kapital'].iloc[-1]:,.2f} $")
    col2.metric("📉 Max. Drawdown", f"{df_perf['drawdown'].max():,.2f} $")
    col3.metric("🎯 Trefferquote", f"{df_perf['win_ratio'].iloc[-1] * 100:.1f} %")
    st.line_chart(df_perf.set_index("timestamp")["kapital"])
except Exception:
    st.warning("Noch keine Kapitaldaten vorhanden.")

st.divider()

# =============================
# TRADE-HISTORIE
# =============================
st.subheader("📒 Letzte Trades")
try:
    df = pd.read_csv("bot_log.csv").sort_values("timestamp", ascending=False)
    df_view = df[["timestamp", "coin", "action", "price", "reward", "leverage", "precision", "fibonacci", "ma200", "news", "fear_greed"]]
    st.dataframe(df_view, height=300)
except Exception:
    st.warning("Noch keine Trades vorhanden.")

# =============================
# STRATEGIE TOP-KOMBIS
# =============================
st.subheader("🏆 Top 10 Strategiekombis")
try:
    with open("top_strategien.json") as f:
        data = json.load(f)
    df_top = pd.DataFrame(data, columns=["Kombi", "Reward"])
    st.dataframe(df_top)
except Exception:
    st.warning("Noch keine Top-Strategien geloggt.")

# =============================
# MUTATION TRACKING
# =============================
st.subheader("🧬 Mutationstracker")
try:
    with open("mutationen_log.json") as f:
        mutationen = json.load(f)
    df_mut = pd.DataFrame(mutationen)
    df_mut["zeit"] = pd.to_datetime(df_mut["zeit"])
    st.dataframe(df_mut.sort_values("zeit", ascending=False), height=200)
except Exception:
    st.warning("Noch keine Mutationen durchgeführt.")

# =============================
# KONFIG & SYSTEMINFO
# =============================
with st.expander("⚙️ Systemstatus & Konfiguration"):
    try:
        with open("bot_config.yaml") as f:
            cfg = f.read()
        st.code(cfg, language="yaml")
    except:
        st.info("Keine Konfigurationsdatei gefunden.")

    if 'df' in locals():
        st.info(f"📊 Insgesamt getradet: {len(df)} Trades")

st.divider()
st.markdown("© 2025 Alex' KI Trading Bot 💹 | Echtzeitvisualisierung powered by Streamlit")
