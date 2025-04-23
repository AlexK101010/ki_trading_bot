# strategy_logger.py – speichert Kombis zur Strategieanalyse

import json
import os

STRATEGIE_LOGFILE = "top_strategien.json"

def log_strategy_result(trade):
    # Erzeuge eine Kombi-Bezeichnung aus relevanten Merkmalen
    combo = f"{trade['fibonacci']} + MA200 + News"
    trade["strategie_combo"] = combo

    # Lade oder initialisiere die Datei
    strategie_data = []
    if os.path.exists(STRATEGIE_LOGFILE):
        with open(STRATEGIE_LOGFILE) as f:
            strategie_data = json.load(f)

    strategie_data.append([combo, trade["reward"]])

    # Nur Top 10
    strategie_data = sorted(strategie_data, key=lambda x: x[1], reverse=True)[:10]

    with open(STRATEGIE_LOGFILE, "w") as f:
        json.dump(strategie_data, f, indent=2)

    return combo
