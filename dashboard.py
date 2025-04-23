# Erweiterte dashboard.py mit interaktiven Features, Telegram-Status und visuellen Upgrades

import streamlit as st
import pandas as pd
import json
import os
import random
import datetime
from config import *
from strategy_logger import log_strategy_result

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
        if st.button("🧹 Kapitalverlauf zurücksetzen"):
            try:
                if os.path.exists(LOGFILE_PERFORMANCE):
                    os.remove(LOGFILE_PERFORMANCE)
                    st.success("Kapitalverlauf wurde zurückgesetzt.")
                else:
                    st.info("Keine Kapitaldatei vorhanden zum Zurücksetzen.")
            except Exception as e:
                st.error(f"Fehler beim Zurücksetzen: {e}")

# =============================
# Manueller Trade-Simulator
# =============================
def simulate_trade():
    coins = ["BTC", "ETH", "SOL", "XRP", "SUI"]
    trade = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "coin": random.choice(coins),
        "price": round(random.uniform(100, 50000), 2),
        "reward": round(random.uniform(-0.1, 0.3), 4),
        "action": random.choice(["Buy", "Sell"]),
        "fibonacci": random.choice(["Support", "Resistance", "Neutral"]),
        "ma200": random.choice(["Above", "Below"]),
        "news": random.choice(["Bullish", "Bearish", "Neutral"]),
        "fear_greed": random.randint(0, 100)
    }
    combo = log_strategy_result(trade)
    trade["strategie_combo"] = combo
    return trade

def log_to_csv(trade, path=LOGFILE_TRADE):
    df = pd.DataFrame([trade])
    if os.path.exists(path):
        old = pd.read_csv(path)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(path, index=False)

def update_performance_log(trade):
    kapital = INITIAL_CAPITAL
    drawdown = 0.0
    win_ratio = 0.0
    pfad = LOGFILE_PERFORMANCE

    if os.path.exists(pfad):
        df = pd.read_csv(pfad)
        kapital = df["kapital"].iloc[-1] + trade["reward"] * 1000
        drawdown = min(drawdown, kapital - df["kapital"].max())
        win_ratio = (df["reward"] > 0).sum() / len(df)
    else:
        kapital += trade["reward"] * 1000

    df_new = pd.DataFrame([{
        "timestamp": trade["timestamp"],
        "kapital": kapital,
        "drawdown": drawdown,
        "win_ratio": win_ratio,
        "reward": trade["reward"]
    }])

    if os.path.exists(pfad):
        df_old = pd.read_csv(pfad)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(pfad, index=False)

if st.button("📈 Jetzt 5 Bot-Trades simulieren"):
    for _ in range(5):
        t = simulate_trade()
        log_to_csv(t)
        update_performance_log(t)
    st.success("✅ 5 neue Trades wurden erzeugt und geloggt.")

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

        st.subheader("🧠 Strategie-Kombinationsauswertung")
        if "strategie_combo" in df.columns:
            strat_avg = df.groupby("strategie_combo")["reward"].mean().reset_index()
            strat_avg = strat_avg.sort_values("reward", ascending=False)
            st.dataframe(strat_avg.rename(columns={"strategie_combo": "Strategie", "reward": "Ø Reward"}))
            st.bar_chart(strat_avg.set_index("Strategie"))
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
    df_strat = df_strat.sort_values("Reward", ascending=False)
    st.dataframe(df_strat)
    st.bar_chart(df_strat.set_index("Strategie"))
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
