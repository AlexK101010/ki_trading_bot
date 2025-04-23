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
# Trainingsstatus-Anzeige
# =============================
st.subheader("🔬 Lernstatus")
with st.expander("📢 Trainingsmodus aktiv"):
    st.info("Der Bot führt aktuell Mutationen durch, um neue Strategiekombinationen zu testen.")

# =============================
# Manueller Trade-Simulator mit Mutation
# =============================
def mutate_strategy(trade):
    mutation_rate = 0.3
    if os.path.exists(LOGFILE_PERFORMANCE):
        df = pd.read_csv(LOGFILE_PERFORMANCE)
        last_reward = df["reward"].iloc[-1]
        if last_reward < 0:
            mutation_rate = 0.6
        elif last_reward > 0.1:
            mutation_rate = 0.1

    if random.random() < mutation_rate:
        original = trade["strategie_combo"]
        parts = original.split(" + ")
        if parts:
            idx = random.randint(0, len(parts)-1)
            options = ["Fibonacci", "RSI", "MA200", "Heatmap", "News", "Trendfolge"]
            parts[idx] = random.choice(options)
        mutated = " + ".join(parts)
        trade["strategie_combo"] = mutated
        return mutated
    return trade["strategie_combo"]

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
    trade["strategie_combo"] = mutate_strategy(trade)
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
# Kapitalverlauf & Trefferquote
# =============================
try:
    df_perf = pd.read_csv(LOGFILE_PERFORMANCE)
    st.subheader("📈 Kapitalverlauf")
    st.metric("Kapital", f"{df_perf['kapital'].iloc[-1]:,.2f} $")
    st.line_chart(df_perf.set_index("timestamp")["kapital"])

    st.subheader("🎯 Trefferquote-Verlauf")
    st.line_chart(df_perf.set_index("timestamp")["win_ratio"])
except:
    st.warning("Kapitaldaten oder Trefferquote konnten nicht geladen werden.")

# =============================
# Letzte Trades anzeigen
# =============================
try:
    df_trades = pd.read_csv(LOGFILE_TRADE)
    st.subheader("📒 Letzte Trades")
    st.dataframe(df_trades.sort_values("timestamp", ascending=False).head(20))
except:
    st.warning("Trade-Daten fehlen oder fehlerhaft.")

# =============================
# Neue Erweiterungen: Erfolgsquote pro Coin & Beste Strategie der Woche
# =============================
try:
    df_all = pd.read_csv(LOGFILE_TRADE)
    st.subheader("📌 Erfolgsquote pro Coin")
    df_all["erfolg"] = df_all["reward"] > 0
    stats = df_all.groupby("coin")["erfolg"].mean().reset_index()
    stats["erfolg"] = (stats["erfolg"] * 100).round(1)
    st.dataframe(stats.rename(columns={"erfolg": "Trefferquote (%)"}))

    st.subheader("🏅 Beste Strategie der Woche")
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    letzte_woche = df_all[df_all["timestamp"] >= (datetime.datetime.utcnow() - datetime.timedelta(days=7))]
    if not letzte_woche.empty:
        top_combo = letzte_woche.groupby("strategie_combo")["reward"].mean().sort_values(ascending=False).head(1)
        st.success(f"Beste Strategie: {top_combo.index[0]} → Ø Reward: {top_combo.values[0]:.4f}")
    else:
        st.info("Noch keine Daten für diese Woche.")

    st.subheader("📊 Top 3 Coins nach Performance")
    top_coins = df_all.groupby("coin")["reward"].mean().sort_values(ascending=False).head(3).reset_index()
    st.bar_chart(top_coins.set_index("coin"))

    st.subheader("⭐ Live-Performance Rating")
    letzte = pd.read_csv(LOGFILE_PERFORMANCE)
    capital = letzte["kapital"].iloc[-1]
    rating = "⭐⭐⭐"
    if capital > INITIAL_CAPITAL * 1.1:
        rating = "⭐⭐⭐⭐⭐"
    elif capital < INITIAL_CAPITAL * 0.9:
        rating = "⭐"
    elif capital < INITIAL_CAPITAL:
        rating = "⭐⭐"
    elif capital > INITIAL_CAPITAL * 1.05:
        rating = "⭐⭐⭐⭐"
    st.success(f"Aktuelle Bewertung: {rating}  (Kapital: {capital:.2f} $)")

    st.subheader("🚨 Drawdown-Warnung")
    letzter_dd = letzte["drawdown"].iloc[-1]
    if letzter_dd < -INITIAL_CAPITAL * 0.2:
        st.error(f"⚠️ Kritischer Drawdown: {letzter_dd:.2f} $")
    else:
        st.info(f"Aktueller Drawdown: {letzter_dd:.2f} $")

except:
    st.warning("Erweiterungsdaten konnten nicht geladen werden.")
