# Erweiterte dashboard.py mit interaktiven Features, Telegram-Status und visuellen Upgrades

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from config import *

st.set_page_config(page_title="KI Trading Bot Dashboard", layout="wide")

st.title("📊 KI Trading Bot Dashboard (Advanced)")
st.markdown("**Status:** Live | 24/7 Online | KI-Modus aktiviert 🧠")

# =============================
# Interaktive Kontrolle
# =============================
if ENABLE_DASHBOARD_CONTROLS:
    with st.sidebar:
        st.header("⚙️ Bot Steuerung")
        if ENABLE_TRAINING_PAUSE:
            training_pause = st.checkbox("🛑 Training pausieren")
        if ENABLE_STRATEGY_RESET:
            if st.button("🔁 Strategien zurücksetzen"):
                st.success("Strategien wurden zurückgesetzt.")

# =============================
# Telegram-Status
# =============================
if ENABLE_TELEGRAM_ALERTS:
    st.subheader("📬 Telegram Status")
    try:
        if os.path.exists(TELEGRAM_LOGFILE):
            with open(TELEGRAM_LOGFILE) as f:
                logs = json.load(f)
            last_sent = logs[-1]["time"]
            st.success(f"Letzte Benachrichtigung: {last_sent}")
        else:
            st.warning("Noch keine Telegram-Nachrichten gesendet.")
    except:
        st.warning("Fehler beim Lesen der Telegram-Logs.")

# =============================
# Kapitalverlauf und Drawdown
# =============================
try:
    df_perf = pd.read_csv(LOGFILE_PERFORMANCE)
    st.metric("📈 Kapital", f"{df_perf['kapital'].iloc[-1]:,.2f} $")
    st.line_chart(df_perf.set_index("timestamp")["kapital"])
    if ENABLE_DRAWDOWN_GRAPH:
        st.line_chart(df_perf.set_index("timestamp")["drawdown"])
except:
    st.warning("Kapitaldaten fehlen oder fehlerhaft.")

# =============================
# Trade-Historie & Heatmap
# =============================
try:
    df = pd.read_csv(LOGFILE_TRADE)
    st.subheader("📒 Letzte Trades")
    st.dataframe(df.tail(50), height=300)
    if ENABLE_HEATMAP:
        st.subheader("🔥 Performance Heatmap pro Coin")
        heatmap_data = df.groupby("coin")["reward"].mean().reset_index()
        st.bar_chart(data=heatmap_data, x="coin", y="reward")
except:
    st.warning("Noch keine Trade-Daten gefunden.")

# =============================
# Strategien & Mutationstracker
# =============================
try:
    st.subheader("🏆 Top Strategiekombis")
    with open(JSON_TOP_STRATEGIEN) as f:
        strat = json.load(f)
    df_strat = pd.DataFrame(strat, columns=["Strategie", "Reward"])
    st.dataframe(df_strat)
except:
    st.warning("Keine Strategiedaten.")

try:
    st.subheader("🧬 Mutationen")
    with open(JSON_MUTATIONEN) as f:
        mut = json.load(f)
    df_mut = pd.DataFrame(mut)
    df_mut["zeit"] = pd.to_datetime(df_mut["zeit"])
    st.dataframe(df_mut.sort_values("zeit", ascending=False), height=200)
except:
    st.warning("Keine Mutationen vorhanden.")

# =============================
# Lernkurve & Wissenstracking
# =============================
if ENABLE_KNOWLEDGE_TRACKING:
    st.subheader("📚 Lernkurve & Wissensentwicklung")
    try:
        df_k = df_perf[["timestamp", "win_ratio"]]
        st.line_chart(df_k.rename(columns={"win_ratio": "Trefferquote"}).set_index("timestamp"))
    except:
        st.info("Noch keine Lernkurve verfügbar.")

# =============================
# Fußzeile
# =============================
st.markdown("---")
st.markdown("© 2025 KI Trading Bot Dashboard • v2.0 mit Streamlit • Entwickelt mit ❤️")
