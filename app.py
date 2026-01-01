import streamlit as st
import pandas as pd
import datetime
import os

# 1. Configurazione
st.set_page_config(page_title="Gym AI Tracker", page_icon="💪")

# 2. Database Locale (File CSV)
DB_FILE = "workout_logs.csv"

# Se il file non esiste, lo creiamo con le colonne necessarie
if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["Data", "Esercizio", "Peso", "Reps", "1RM"])
    df_init.to_csv(DB_FILE, index=False)

# Aggiungi dati di esempio se il file è vuoto (per debug)
df = pd.read_csv(DB_FILE)
if df.empty:
    sample_data = [
        {"Data": "2025-12-25", "Esercizio": "Panca Piana", "Peso": 70.0, "Reps": 10, "1RM": 77.0},
        {"Data": "2025-12-26", "Esercizio": "Panca Piana", "Peso": 75.0, "Reps": 8, "1RM": 82.5},
        {"Data": "2025-12-27", "Esercizio": "Squat", "Peso": 90.0, "Reps": 8, "1RM": 99.0},
        {"Data": "2025-12-28", "Esercizio": "Squat", "Peso": 95.0, "Reps": 6, "1RM": 102.14},
    ]
    df_sample = pd.DataFrame(sample_data)
    df_sample.to_csv(DB_FILE, index=False)

# 3. Interfaccia Sidebar
st.sidebar.header("📝 Registra Serie")
esercizio = st.sidebar.selectbox("Esercizio", ["Panca Piana", "Squat", "Stacco", "Military Press"])
peso = st.sidebar.number_input("Peso (kg)", 0.0, 300.0, 60.0, 2.5)
reps = st.sidebar.number_input("Reps", 1, 30, 8)

if st.sidebar.button("Salva Allenamento"):
    # Calcolo 1RM Reale (Formula di Epley)
    one_rm = round(peso * (1 + reps / 30), 2)
    nuovo_dato = pd.DataFrame([[datetime.date.today(), esercizio, peso, reps, one_rm]], 
                             columns=["Data", "Esercizio", "Peso", "Reps", "1RM"])
    
    # Salvataggio persistente
    nuovo_dato.to_csv(DB_FILE, mode='a', header=False, index=False)
    st.sidebar.success("Salvato!")
    st.rerun()

# 4. Dashboard Principale
st.title("💪 Gym AI Data Analyzer")

# Carichiamo i dati dal CSV
df = pd.read_csv(DB_FILE)

if not df.empty:
    # Trasformiamo la colonna Data in formato leggibile da pandas
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Filtro per Esercizio
    focus = st.selectbox("Analizza i tuoi progressi:", df["Esercizio"].unique())
    df_filtered = df[df["Esercizio"] == focus].sort_values("Data")

    # Metric Cards
    col1, col2 = st.columns(2)
    if not df_filtered.empty:
        ultimo_rm = df_filtered["1RM"].iloc[-1]
        precedente_rm = df_filtered["1RM"].iloc[-2] if len(df_filtered) > 1 else ultimo_rm
        delta = round(ultimo_rm - precedente_rm, 2)
        
        col1.metric("Massimale Attuale", f"{ultimo_rm} kg", delta=f"{delta} kg")
        col2.metric("Record Personale", f"{df_filtered['1RM'].max()} kg")

    # 📈 Grafico REALE (Non più simulato!)
    st.write(f"#### Andamento 1RM: {focus}")
    st.line_chart(df_filtered.set_index("Data")["1RM"])

    # 🤖 LOGICA AI PREDIZIONE (Basi di Regressione Lineare)
    st.write("---")
    st.write("### 🤖 Previsione AI")
    if len(df_filtered) > 2:
        # Calcoliamo la pendenza della crescita (semplificata)
        progressione = (df_filtered["1RM"].iloc[-1] - df_filtered["1RM"].iloc[0]) / len(df_filtered)
        prossimo_target = round(df_filtered["1RM"].iloc[-1] + progressione, 1)
        
        st.success(f"Basato sulla tua velocità di crescita, il tuo target per la prossima settimana è **{prossimo_target} kg** di Massimale.")
    else:
        st.info("Ho bisogno di almeno 3 allenamenti registrati per prevedere la tua crescita.")

else:
    st.warning("Il database è vuoto. Inserisci i dati nella sidebar per vedere la magia dell'AI!")